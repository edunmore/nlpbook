from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import os
from pathlib import Path
from typing import List, Optional
import sys
import json

app = FastAPI(title="Book Writer GUI")

# Allow CORS for dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"
IMAGES_DIR = WORKSPACE_ROOT / "images"
PROMPTS_DIR = WORKSPACE_ROOT / "prompts"
SCRIPTS_DIR = WORKSPACE_ROOT / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "refine_chapters.py"

# Ensure directories exist
os.makedirs(WORLDS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Mount images
app.mount("/api/images", StaticFiles(directory=IMAGES_DIR), name="images")

class UpdateFeedbackRequest(BaseModel):
    content: str

class RefineRequest(BaseModel):
    chapter: Optional[str] = None # e.g. "001"
    model: str = "gemini"
    world: str = "default"
    type: str = "custom" # custom, writer, cc, se, qa, po

class WorldRequest(BaseModel):
    name: str

class GenerateRequest(BaseModel):
    world: str = "default"
    count: int = 5
    start: int = 1

def get_world_paths(world_name):
    world_dir = WORLDS_DIR / world_name
    return {
        "root": world_dir,
        "canon": world_dir / "canon",
        "chapters": world_dir / "chapters",
        "meta": world_dir / "chapters" / "meta",
        "config": world_dir / "canon" / "world_config.json"
    }

# --- Worlds API ---

@app.get("/api/worlds")
def list_worlds():
    if not WORLDS_DIR.exists():
        return []
    items = [d.name for d in WORLDS_DIR.iterdir() if d.is_dir()]
    return sorted(items)

@app.post("/api/worlds")
def create_world(req: WorldRequest):
    paths = get_world_paths(req.name)
    if paths["root"].exists():
         raise HTTPException(status_code=400, detail="World already exists")
    
    os.makedirs(paths["canon"], exist_ok=True)
    os.makedirs(paths["chapters"], exist_ok=True)
    os.makedirs(paths["meta"], exist_ok=True)
    os.makedirs(paths["root"] / "planning" / "chapter-cards", exist_ok=True)
    os.makedirs(paths["root"] / "history", exist_ok=True)
    
    # Copy essential canon files from default world
    default_canon = WORLDS_DIR / "default" / "canon"
    import shutil
    
    # Files to copy as-is (universal rules)
    files_to_copy = [
        "BANNED_TERMS.txt", 
        "STYLE_RULES.md", 
        "RECURRING_MOTIFS.md",
        "WORLD_RULES.md",
        "ENTITY_TEMPLATES.md",
        "STYLE_GUIDE.md"
    ]
    for filename in files_to_copy:
        src = default_canon / filename
        dst = paths["canon"] / filename
        if src.exists():
            shutil.copy(src, dst)
    
    # Create template files for world-specific canon
    templates = {
        "SERIES_BIBLE.md": f"""# Series Bible — {req.name}

## Premise
[Describe your story premise هنا. What is the fundamental conflict?]

## Deep Theme
[What is this story REALLY about? (e.g., 'The cost of absolute control', 'Finding connection in a digital void')]

## Main Cast
- **Protagonist**: [Name] - [Specific Role and internal conflict]
- **Antagonist/Friction**: [Name] - [How they challenge the protagonist]
- **Mentor/Guide**: [Name] - [The source of NLP concepts]

## Setting
[Describe the core locations and the 'vibe' of the world]
""",
        "CONTINUITY_LEDGER.md": f"""# Continuity Ledger — {req.name}

## Facts & Truths
- [Key fact about the world that must never be broken]

## Timeline
- **Event A**: [Description]
- **Event B**: [Description]

## Character Progress
- **[Character Name]**: [Current state/location/knowledge]
""",
        "OPEN_LOOPS.md": f"# Open Loops — {req.name}\n\n- LOOP-01: [First unresolved plot thread]. Status: OPEN.\n"
    }
    for filename, content in templates.items():
        dst = paths["canon"] / filename
        if not dst.exists():
            with open(dst, "w") as f:
                f.write(content)
    
    # Create default config with source_path placeholder
    # Attempt to find common source paths
    possible_sources = ["NLP", "source", "research"]
    found_source = ""
    for ps in possible_sources:
        if (WORKSPACE_ROOT / ps).exists():
            found_source = ps
            break

    default_config = {
        "title": req.name,
        "characters": [
            {"name": "Protagonist", "role": "Main", "description": "TBD"},
            {"name": "Mentor", "role": "Guide", "description": "TBD"}
        ],
        "setting": "Modern City",
        "theme": "Discovery",
        "source_path": found_source,
        "workflow_stage": "brainstorm"
    }
    with open(paths["config"], "w") as f:
        json.dump(default_config, f, indent=2)
        
    return {"status": "ok", "name": req.name}


# --- Chapters API ---

@app.get("/api/chapters")
def list_chapters(world: str = "default"):
    paths = get_world_paths(world)
    if not paths["chapters"].exists():
        return []
    files = sorted(paths["chapters"].glob("CH*.md"))
    return [{"filename": f.name, "path": str(f)} for f in files]

@app.get("/api/chapters/{filename:path}")
def get_chapter(filename: str, world: str = "default"):
    paths = get_world_paths(world)
    path = paths["chapters"] / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    with open(path, "r") as f:
        content = f.read()
        
    # Get feedback if exists
    feedback_path = paths["meta"] / f"{filename}.feedback.md"
    feedback = ""
    if feedback_path.exists():
        with open(feedback_path, "r") as f:
            feedback = f.read()
            
    return {"content": content, "feedback": feedback, "filename": filename}

@app.get("/api/global-instructions")
def get_global_instructions():
    """Get global improvement ideas."""
    path = PROMPTS_DIR / "IMPROVEMENT_IDEAS.md"
    if not path.exists():
        return {"content": ""}
    with open(path, "r") as f:
        return {"content": f.read()}

@app.post("/api/global-instructions")
def save_global_instructions(body: UpdateFeedbackRequest):
    """Update global improvement ideas."""
    path = PROMPTS_DIR / "IMPROVEMENT_IDEAS.md"
    with open(path, "w") as f:
        f.write(body.content)
    return {"status": "ok"}

@app.post("/api/chapters/{filename}/feedback")
def save_chapter_feedback(filename: str, body: UpdateFeedbackRequest, world: str = "default"):
    paths = get_world_paths(world)
    os.makedirs(paths["meta"], exist_ok=True)
    feedback_path = paths["meta"] / f"{filename}.feedback.md"
    with open(feedback_path, "w") as f:
        f.write(body.content)
    return {"status": "ok"}

@app.post("/api/refine")
def run_refinement(req: RefineRequest):
    # Note: script needs verify/update to support --world if we want strict separation
    # But refine script currently works on absolute paths in get_chapters if needed, 
    # BUT refine_chapters.py is hardcoded to workspace/chapters.
    # We should update refine_chapters.py OR just rely on generating dynamic path args.
    # For now, let's assume we pass a world arg if script supports it (it doesn't yet in this code block).
    # TODO: Update refine_chapters.py to take --world argument.
    
    # We need to update refine_chapters.py to support world. For now, let's just create a wrapper here or update script.
    # Actually, previous plan didn't explicitly say refine_chapters.py was updated, but "Refactor Scripts" implies it.
    # Let's assume refine_chapters.py WAS updated in previous steps or needs to be.
    # Wait, I only updated generate_*.py. I missed refine_chapters.py.
    # I will fix refine_chapters.py in a separate tool call.
    
    # Passing --world to refine script
    cmd = [sys.executable, str(SCRIPT_PATH), "--model", req.model, "--world", req.world, "--type", req.type]
    if req.chapter:
        cmd.extend(["--chapter", req.chapter])
        
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return {"status": "error", "output": result.stderr}
        return {"status": "ok", "output": result.stdout}
    except Exception as e:
        return {"status": "error", "output": str(e)}

# --- Background Process & Logging ---

import threading
import subprocess
import queue
import time

# Global Log Buffer
log_buffer = []
MAX_LOG_LINES = 1000

def append_log(line):
    global log_buffer
    timestamp = time.strftime("%H:%M:%S")
    log_buffer.append(f"[{timestamp}] {line}")
    if len(log_buffer) > MAX_LOG_LINES:
        log_buffer.pop(0)

def run_script_threaded(cmd):
    """Runs a script and pipes output to global log."""
    def target():
        append_log(f"COMMAND: {' '.join(cmd)}")
        try:
            # Use Popen to capture stdout/stderr in real-time
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                bufsize=1, 
                universal_newlines=True
            )
            
            # Read stdout line by line
            for line in process.stdout:
                append_log(line.strip())
                
            # Read any stderr remaining
            stderr = process.stderr.read()
            if stderr:
                append_log(f"ERROR: {stderr}")
                
            process.wait()
            append_log(f"Process finished with code {process.returncode}")
            
        except Exception as e:
            append_log(f"EXCEPTION: {str(e)}")

    thread = threading.Thread(target=target)
    thread.start()
    return {"status": "started"}

@app.get("/api/logs")
def get_logs():
    return {"logs": log_buffer}

# --- World Builder Endpoints ---

@app.get("/api/world-config")
def get_world_config(world: str = "default"):
    paths = get_world_paths(world)
    if not paths["config"].exists():
        return {}
    with open(paths["config"], "r") as f:
        return json.load(f)

@app.post("/api/world-config")
def save_world_config(config: dict = Body(...), world: str = "default"):
    paths = get_world_paths(world)
    with open(paths["config"], "w") as f:
        json.dump(config, f, indent=2)
    return {"status": "ok"}

@app.post("/api/generate/storyline")
def generate_storyline(req: GenerateRequest):
    script = WORKSPACE_ROOT / "scripts" / "generate_storyline.py"
    cmd = [sys.executable, str(script), "--world", req.world]
    return run_script_threaded(cmd)

@app.post("/api/generate/chapters")
def generate_chapters(req: GenerateRequest):
    script = WORKSPACE_ROOT / "scripts" / "generate_chapters.py"
    cmd = [sys.executable, str(script), "--count", str(req.count), "--start", str(req.start), "--world", req.world]
    return run_script_threaded(cmd)

@app.post("/api/generate/characters")
def generate_characters(req: GenerateRequest):
    script = WORKSPACE_ROOT / "scripts" / "generate_characters.py"
    cmd = [sys.executable, str(script), "--world", req.world, "--count", str(req.count)]
    return run_script_threaded(cmd)

@app.post("/api/generate/cards")
def generate_cards(req: GenerateRequest):
    script = SCRIPTS_DIR / "generate_chapter_cards.py"
    cmd = [sys.executable, str(script), "--world", req.world, "--count", str(req.count), "--start", str(req.start)]
    return run_script_threaded(cmd)

@app.post("/api/generate/brainstorm")
def generate_brainstorm(req: GenerateRequest):
    script = SCRIPTS_DIR / "generate_brainstorm_iterative.py"
    cmd = [sys.executable, str(script), "--world", req.world, "--max-files", str(req.count)]
    return run_script_threaded(cmd)

@app.post("/api/generate/map")
def generate_map(req: GenerateRequest):
    script = SCRIPTS_DIR / "generate_chapter_map.py"
    cmd = [sys.executable, str(script), "--world", req.world, "--count", str(req.count)]
    return run_script_threaded(cmd)

@app.post("/api/generate/world")
def generate_world(req: GenerateRequest):
    script = WORKSPACE_ROOT / "scripts" / "generate_world.py"
    cmd = [sys.executable, str(script), "--world", req.world]
    return run_script_threaded(cmd)

# --- Brainstorm Review API ---

@app.get("/api/brainstorm")
def get_brainstorm(world: str = "default"):
    """Get brainstorm concepts for review."""
    paths = get_world_paths(world)
    brainstorm_path = paths["root"] / "planning" / "BRAINSTORM_RAW.json"
    if not brainstorm_path.exists():
        return {"concepts": [], "status": "not_started"}
    with open(brainstorm_path, "r") as f:
        concepts = json.load(f)
    return {"concepts": concepts, "status": "in_review"}

class BrainstormUpdateRequest(BaseModel):
    concepts: list
    world: str = "default"

@app.post("/api/brainstorm")
def save_brainstorm(req: BrainstormUpdateRequest):
    """Save updated brainstorm (ratings, deletions)."""
    paths = get_world_paths(req.world)
    brainstorm_path = paths["root"] / "planning" / "BRAINSTORM_RAW.json"
    os.makedirs(paths["root"] / "planning", exist_ok=True)
    with open(brainstorm_path, "w") as f:
        json.dump(req.concepts, f, indent=2)
    return {"status": "ok"}

@app.post("/api/brainstorm/approve")
def approve_brainstorm(world: str = "default"):
    """Mark brainstorm as approved, update workflow stage."""
    paths = get_world_paths(world)
    config_path = paths["config"]
    with open(config_path, "r") as f:
        config = json.load(f)
    config["workflow_stage"] = "map_generate"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    return {"status": "ok", "next_stage": "map_generate"}

# --- Chapter Map Review API ---

@app.get("/api/chapter-map")
def get_chapter_map(world: str = "default"):
    """Get chapter map for review."""
    paths = get_world_paths(world)
    map_path = paths["root"] / "planning" / "CHAPTER_MAP.md"
    if not map_path.exists():
        return {"content": "", "status": "not_started"}
    with open(map_path, "r") as f:
        content = f.read()
    return {"content": content, "status": "in_review"}

@app.post("/api/chapter-map")
def save_chapter_map(content: str = Body(...), world: str = "default"):
    """Save edited chapter map."""
    paths = get_world_paths(world)
    map_path = paths["root"] / "planning" / "CHAPTER_MAP.md"
    os.makedirs(paths["root"] / "planning", exist_ok=True)
    with open(map_path, "w") as f:
        f.write(content)
    return {"status": "ok"}

@app.post("/api/chapter-map/approve")
def approve_chapter_map(world: str = "default"):
    """Mark chapter map as approved."""
    paths = get_world_paths(world)
    config_path = paths["config"]
    with open(config_path, "r") as f:
        config = json.load(f)
    config["workflow_stage"] = "cards_generate"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    return {"status": "ok", "next_stage": "cards_generate"}

# --- Steering API (Prompts/Process/Canon/Chapter Cards) ---

PATH_MAP = {
    "prompts": PROMPTS_DIR,
    "process": WORKSPACE_ROOT / "process",
    "chapter-cards": WORKSPACE_ROOT / "planning" / "chapter-cards",
    # Canon is handled relative to world
}

class SteeringFileRequest(BaseModel):
    category: str # "prompts", "process", "canon", "chapter-cards"
    filename: str
    content: str
    world: str = "default"

@app.get("/api/steering/files")
def list_steering_files(category: str, world: str = "default"):
    """
    List files available for the category.
    Merges global defaults with world-specific overrides.
    """
    # 1. Identify Global Source
    global_dir = None
    if category in PATH_MAP:
        global_dir = PATH_MAP[category]
    
    # 2. Identify World Source
    world_paths = get_world_paths(world)
    world_dir = None
    if category == "prompts":
        world_dir = world_paths["root"] / "prompts"
    elif category == "process":
        world_dir = world_paths["root"] / "process"
    elif category == "canon":
        world_dir = world_paths["canon"]
        global_dir = None # Canon has no global fallback
    elif category == "chapter-cards":
        # Check if world has specific planning/chapter-cards?
        # User structure update implied worlds might have their own planning?
        # For now, let's assume world/planning/chapter-cards
        world_dir = world_paths["root"] / "planning" / "chapter-cards"

    files = set()
    
    # Scan Global
    if global_dir and global_dir.exists():
        for f in global_dir.glob("*.md"):
            files.add(f.name)
            
    # Scan World (to find overrides or world-only files)
    if world_dir and world_dir.exists():
        for f in world_dir.glob("*.md"):
            files.add(f.name)
            
    return sorted(list(files))

@app.get("/api/steering/content")
def get_steering_content(category: str, filename: str, world: str = "default"):
    """
    Get content. 
    Priority: World Specific -> Global Default.
    """
    world_paths = get_world_paths(world)
    
    # Determine potential paths
    target_path = None
    source = "global"

    # Define world local path
    world_local = None
    if category == "prompts":
        world_local = world_paths["root"] / "prompts" / filename
    elif category == "process":
        world_local = world_paths["root"] / "process" / filename
    elif category == "canon":
        world_local = world_paths["canon"] / filename
        source = "world" # Canon is always world
    elif category == "chapter-cards":
         world_local = world_paths["root"] / "planning" / "chapter-cards" / filename

    # Check World First
    if world_local and world_local.exists():
        target_path = world_local
        source = "world"
    
    # Fallback to Global
    if not target_path and category in PATH_MAP:
        global_path = PATH_MAP[category] / filename
        if global_path.exists():
            target_path = global_path
            source = "global"
            
    if not target_path or not target_path.exists():
         raise HTTPException(status_code=404, detail="File not found")
         
    with open(target_path, "r") as f:
        content = f.read()
        
    return {"content": content, "source": source, "path": str(target_path)}

@app.post("/api/steering/content")
def save_steering_content(req: SteeringFileRequest):
    """
    Save content.
    ALWAYS saves to the World directory (creating an override if it was global).
    """
    world_paths = get_world_paths(req.world)
    target_dir = None
    
    if req.category == "prompts":
        target_dir = world_paths["root"] / "prompts"
    elif req.category == "process":
        target_dir = world_paths["root"] / "process"
    elif req.category == "canon":
        target_dir = world_paths["canon"]
    elif req.category == "chapter-cards":
        target_dir = world_paths["root"] / "planning" / "chapter-cards"
        
    if not target_dir:
        raise HTTPException(status_code=400, detail="Invalid category")
        
    os.makedirs(target_dir, exist_ok=True)
    target_path = target_dir / req.filename
    
    with open(target_path, "w") as f:
        f.write(req.content)
        
    return {"status": "ok", "path": str(target_path)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
