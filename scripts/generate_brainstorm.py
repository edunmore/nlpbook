#!/usr/bin/env python3
"""
Generate Brainstorm Script

Reads source material from `worlds/{world}/source/` (or configured path)
and generates a list of ideas using `BRAINSTORM_GENERATOR.md`.
"""

import argparse
import json
import os
import sys
import glob
from pathlib import Path

# Add scripts dir to python path to import agent_utils
sys.path.append(str(Path(__file__).resolve().parent))
from agent_utils import run_agent

# Config
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"
PROMPTS_DIR = WORKSPACE_ROOT / "prompts"

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        sys.exit(1)

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def load_template(world_dir, filename):
    # 1. World Override
    world_prompt = world_dir / "prompts" / filename
    if world_prompt.exists():
        return load_file(world_prompt)
    # 2. Global Default
    global_prompt = PROMPTS_DIR / filename
    if global_prompt.exists():
        return load_file(global_prompt)
    return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini", help="CLI tool to use")
    parser.add_argument("--world", default="default", help="World name")
    parser.add_argument("--count", type=int, default=10, help="Number of ideas to generate")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    if not world_dir.exists():
        print(f"World '{args.world}' not found")
        sys.exit(1)

    config_path = world_dir / "canon" / "world_config.json"
    if not config_path.exists():
        print("Config not found")
        sys.exit(1)

    config = load_json(config_path)
    
    # Identify Source Path
    source_path_str = config.get("source_path", None)
    if not source_path_str:
        # Default to worlds/{world}/source
        source_dir = world_dir / "source"
    else:
        # Resolve path
        if source_path_str.startswith("/"):
            source_dir = Path(source_path_str)
        else:
            source_dir = WORKSPACE_ROOT / source_path_str
            
    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        print("Please set 'source_path' in world_config.json or create a 'source' folder.")
        sys.exit(1)
        
    # Read Source Files
    # We might have too much text. For V1, let's read first 5 files or up to X chars.
    source_files = sorted(glob.glob(str(source_dir / "*.txt")) + glob.glob(str(source_dir / "*.md")))
    if not source_files:
        print(f"No text files found in {source_dir}")
        sys.exit(1)
        
    print(f"Found {len(source_files)} source files in {source_dir}")
    
    # Simple strategy: Concatenate snippets from first 10 files
    collapsed_source = ""
    read_count = 0
    MAX_CHARS = 30000 # Keep context reasonable
    
    for fpath in source_files:
        content = load_file(fpath)
        # Take first 2000 chars of each file as a digest
        snippet = f"\n--- FILE: {Path(fpath).name} ---\n{content[:2000]}...\n"
        collapsed_source += snippet
        read_count += 1
        if len(collapsed_source) > MAX_CHARS:
            break
            
    # Load Template
    template = load_template(world_dir, "BRAINSTORM_GENERATOR.md")
    if not template:
        print("Template BRAINSTORM_GENERATOR.md not found.")
        sys.exit(1)
        
    # Inject Context
    chars_text = ""
    for char in config.get('characters', []):
        chars_text += f"- {char['name']} ({char['role']}): {char.get('description', '')}\n"

    prompt = template.replace("{{SOURCE_COUNT}}", str(read_count))
    prompt = prompt.replace("{{SOURCE_MATERIAL_EXCERPT}}", collapsed_source)
    prompt = prompt.replace("{{TITLE}}", config.get('title', 'Untitled'))
    prompt = prompt.replace("{{THEME}}", config.get('theme', ''))
    prompt = prompt.replace("{{CHARACTERS}}", chars_text)
    prompt = prompt.replace("{{COUNT}}", str(args.count))
    
    # Run Agent
    output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="brainstorm_ideas")
    
    if output:
        # Save to planning/BRAINSTORM.md
        planning_dir = world_dir / "planning"
        os.makedirs(planning_dir, exist_ok=True)
        
        # Clean JSON markdown if present
        clean_output = output.strip()
        if clean_output.startswith("```json"):
            clean_output = clean_output[7:]
        if clean_output.endswith("```"):
             clean_output = clean_output[:-3]
        
        # We want to save the RAW JSON for the script to use, but maybe also a readable MD?
        # For now, let's just save the text output as BRAINSTORM.md
        # If the user wants to refine it, they can edit it.
        # But wait, generate_chapters needs to READ this. It should be structured.
        
        # Let's save as JSON
        output_path = planning_dir / "BRAINSTORM.json"
        try:
             # Try to validate JSON
             data = json.loads(clean_output)
             with open(output_path, "w", encoding="utf-8") as f:
                 json.dump(data, f, indent=2)
             print(f"Saved brainstorm list to {output_path}")
             
             # Also save a readable MD version for the user
             md_path = planning_dir / "BRAINSTORM.md"
             md_content = "# Brainstormed Ideas\n\n"
             for item in data:
                 md_content += f"## {item.get('title')}\n"
                 md_content += f"**Source**: {item.get('source_concept')}\n"
                 md_content += f"**Plot**: {item.get('plot_beat')}\n\n"
                 md_content += f"{item.get('synopsis')}\n\n"
             with open(md_path, "w", encoding="utf-8") as f:
                 f.write(md_content)
             print(f"Saved readable brainstorm to {md_path}")
             
        except json.JSONDecodeError:
            print("Warning: Agent output was not valid JSON. Saving raw output to BRAINSTORM.md")
            with open(planning_dir / "BRAINSTORM.md", "w", encoding="utf-8") as f:
                f.write(output)

if __name__ == "__main__":
    main()
