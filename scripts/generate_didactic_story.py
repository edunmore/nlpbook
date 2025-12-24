#!/usr/bin/env python3
"""
Didactic Fiction Generator
Iterates through source materials recursively to build a "Phoenix Project" style business fable.
"""

import argparse
import glob
import os
import sys
import json
from pathlib import Path

# Add scripts dir to python path
sys.path.append(str(Path(__file__).resolve().parent))
from agent_utils import run_agent, load_prompt

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", required=True, help="World name")
    parser.add_argument("--model", default="gemini", help="Model to use")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    source_dir = world_dir / "source"
    chapters_dir = world_dir / "chapters"
    os.makedirs(chapters_dir, exist_ok=True)

    # 1. Validate Environment
    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        return

    # 2. Load Prompt
    prompt_template = load_prompt(world_dir, "AGENT_DIDACTIC_ARCHITECT.md")
    if not prompt_template:
        print("AGENT_DIDACTIC_ARCHITECT.md not found.")
        sys.exit(1)

    # 3. Gather Source Files
    source_files = sorted(glob.glob(str(source_dir / "*.md"))) + sorted(glob.glob(str(source_dir / "*.txt")))
    if not source_files:
        print("No source files found.")
        return

    # 4. Initialize Narrative State
    narrative_state = "START OF STORY. No events have occurred yet. The Protagonist is waiting for the first challenge."
    full_story_manuscript = "# THE DIDACTIC FABLE\n\n"

    print(f"Found {len(source_files)} source files. Beginning recursive generation...")

    # 5. Recursive Loop
    for i, src_file in enumerate(source_files):
        src_name = Path(src_file).stem
        print(f"[{i+1}/{len(source_files)}] Processing {src_name}...")
        
        content = load_file(src_file)
        
        # Inject Context
        prompt = prompt_template.replace("{{NARRATIVE_STATE}}", narrative_state) # If we used placeholders, but we'll append for now
        
        # Construct the Runtime Prompt
        # We manually structure the input blocks as defined in the prompt's "INPUT STREAMS" section.
        runtime_input = f"""
{prompt_template}

---

# RUNTIME INPUTS

## 1. CURRENT SOURCE MATERIAL (The Lesson)
{content}

## 2. NARRATIVE STATE (Previous Output)
{narrative_state}

## 3. CAST MANIFESTO
(Using Default - Override here if needed)
"""

        # Run Agent
        output = run_agent(
            runtime_input, 
            model=args.model, 
            world_dir=world_dir, 
            task_name=f"didactic_{src_name}", 
            cwd=world_dir
        )

        if output:
            # Append to manuscript
            full_story_manuscript += f"## Chapter {i+1}: {src_name}\n\n{output}\n\n---\n\n"
            
            # Update Narrative State with the *entire* output of this step
            # The agent is designed to read the previous output to know where it is.
            # For a long story, we might want to summarize this, but for now, passing the raw output works for short sequences.
            narrative_state = output
            
            # Save intermediate result
            with open(chapters_dir / "DIDACTIC_STORY_DRAFT.md", "w", encoding="utf-8") as f:
                f.write(full_story_manuscript)

    print(f"Generation complete. Saved to {chapters_dir / 'DIDACTIC_STORY_DRAFT.md'}")

if __name__ == "__main__":
    main()
