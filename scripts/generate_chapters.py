#!/usr/bin/env python3
"""
Generate Chapters Script

Reads `canon/world_config.json` and `canon/TIMELINE.md`.
Generates chapters based on this context. 
WARNING: This is a devastatingly simple version that just generates a fixed number of chapters 
based on the timeline, or simply one chapter per "Beat" if we parse it.
For this MVP, let's assume we want to generate N chapters that fit the timeline.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Add scripts dir to python path to import agent_utils
sys.path.append(str(Path(__file__).resolve().parent))
from agent_utils import run_agent, load_prompt

# Config
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return ""

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        sys.exit(1)

def resolve_file_content(match_text, world_dir, args):
    """
    Resolves syntax like canon/SERIES_BIBLE.md or planning/chapter-cards/CH001.md
    """
    path_str = match_text.strip()
    
    # Handle dynamic substitution in path (e.g. CH{{CHAPTER_NUM}})
    path_str = path_str.replace("{{CHAPTER_NUM}}", f"{args.chap_num}")
    
    # Logic:
    # If path starts with canon/ -> check world/canon/ -> check default/canon/ -> error
    # If path starts with planning/ -> check world/planning/ -> check root planning/ ?? 
    # Actually, planning is currently root, but might become world specific.
    # User request implies "defaults in each world"
    
    # Let's try to find it relative to world root first
    target = world_dir / path_str
    if target.exists():
        return load_file(target)
        
    # Fallback for "canon/" to worlds/NEWORLDTEMPLATE/canon if we are in a custom world?
    # Or maybe just check workspace root?
    target = WORKSPACE_ROOT / path_str
    if target.exists():
        return load_file(target)
        
    return f"[MISSING FILE: {path_str}]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini", help="CLI tool to use")
    parser.add_argument("--count", type=int, default=5, help="Number of chapters to generate")
    parser.add_argument("--start", type=int, default=1, help="Start chapter number")
    parser.add_argument("--world", default="NEWORLDTEMPLATE", help="World name (directory in worlds/)")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    if not world_dir.exists():
        print(f"World '{args.world}' not found")
        sys.exit(1)

    chapters_dir = world_dir / "chapters"
    os.makedirs(chapters_dir, exist_ok=True)
    
    print(f"Generating {args.count} chapters for world '{args.world}' (Data-Driven)...")
    
    # Load Prompt
    prompt_template = load_prompt(world_dir, "WRITER_INSTRUCTIONS.md")
    if not prompt_template:
        print("Error: Could not find WRITER_INSTRUCTIONS.md in world or global prompts.")
        sys.exit(1)

    for i in range(args.start, args.start + args.count):
        chap_num = f"{i:03}"
        args.chap_num = chap_num
        print(f"Generating CH{chap_num}...")
        
        # 1. Basic Variable Substitution
        prompt = template_content
        prompt = prompt.replace("{{TASK_TITLE}}", f"Generate Chapter {i}")
        prompt = prompt.replace("{{CHAPTER_NUM}}", chap_num)
        prompt = prompt.replace("{{TASK_ID}}", f"GEN-{chap_num}")
        prompt = prompt.replace("{{TASK_DESCRIPTION}}", f"Write Chapter {i} based on the timeline and chapter card.")
        prompt = prompt.replace("{{TASK_NOTES}}", "Ensure strict adherence to style rules.")
        
        # 2. File Content Injection
        # We look for lines starting with "- " that look like file paths in the "Required Inputs" section?
        # A robust way is a regex or just line scanning manually if we know the format.
        # But wait, the template might just list them.
        # Let's verify WRITER_INSTRUCTIONS format.
        # It has a section:
        # ## Required Inputs (Read These Files)
        # - canon/SERIES_BIBLE.md
        # ...
        
        # We will iterate lines, if we see a file format we recognize, we Inject it?
        # Or does the context window need the CONTENT?
        # Yes, we must read the files and Paste them into the prompt.
        
        final_prompt_lines = []
        for line in prompt.split('\n'):
            stripped = line.strip()
            # Heuristic for file inclusion: line starting with "- " containing ".md" or ".txt"
            # Support suffix like " (if exists)"
            if stripped.startswith("- ") and ("/" in stripped):
                # Extract potential filename
                # content usually is "- path/to/file.md" or "- path/to/file.md (notes)"
                parts = stripped[2:].split(' ')
                potential_path = parts[0]
                
                if potential_path.endswith(".md") or potential_path.endswith(".txt"):
                    filename = potential_path
                    content = resolve_file_content(filename, world_dir, args)
                    
                    # If content indicates missing file, check if it was marked optional?
                    # valid return from resolve_file_content is the content string.
                    # If it returns [MISSING FILE...], we might want to skip if it was "if exists"
                    
                    if "[MISSING FILE" in content and "(if exists)" in stripped:
                         # Skip optional missing file
                         pass 
                    else:
                        final_prompt_lines.append(f"\n--- FILE: {filename} ---\n{content}\n--- END {filename} ---\n")
                else:
                    final_prompt_lines.append(line)
            else:
                final_prompt_lines.append(line)
                
        final_prompt = "\n".join(final_prompt_lines)
        
        # Run Agent
        output = run_agent(final_prompt, model=args.model, world_dir=world_dir, task_name=f"generate_chapter_{chap_num}", cwd=world_dir)
        
        if output:
            first_line = output.strip().split('\n')[0]
            safe_title = "Generated"
            if first_line.startswith("#"):
                safe_title = first_line.replace("#", "").strip().replace(":", "").replace(" ", "-")
            
            filename = f"CH{chap_num}-{safe_title}.md"
            path = chapters_dir / filename
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Saved {filename}")

if __name__ == "__main__":
    main()
