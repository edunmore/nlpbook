#!/usr/bin/env python3
"""
Generate Storyline Script

Reads `canon/world_config.json` and generates `canon/TIMELINE.md`.
"""

import argparse
import json
import os
import subprocess
import sys
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini", help="CLI tool to use")
    parser.add_argument("--world", default="default", help="World name (directory in worlds/)")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    if not world_dir.exists():
        print(f"World '{args.world}' not found at {world_dir}")
        sys.exit(1)

    canon_dir = world_dir / "canon"
    config_file = canon_dir / "world_config.json"
    timeline_file = canon_dir / "TIMELINE.md"

    if not config_file.exists():
        print(f"Config not found at {config_file}")
        sys.exit(1)

    config = load_json(config_file)
    
    # Select Trigger (Steering File)
    # Check for World Specific Override first
    trigger_name = "STORY_GENERATOR.md"
    trigger_path = world_dir / "prompts" / trigger_name
    
    if not trigger_path.exists():
         trigger_path = PROMPTS_DIR / trigger_name
         
    if not trigger_path.exists():
        print(f"Prompt template not found: {trigger_name}")
        sys.exit(1)
        
    print(f"Using Prompt Template: {trigger_path}")
    prompt_template = load_file(trigger_path)

    # Format character list
    chars_text = ""
    for char in config.get('characters', []):
        chars_text += f"- **{char['name']}** ({char['role']}): {char.get('description', '')}\n"

    # Inject Context
    prompt = prompt_template.replace("{{TITLE}}", config.get('title', 'Untitled'))
    prompt = prompt.replace("{{CHARACTERS}}", chars_text)
    prompt = prompt.replace("{{SETTING}}", config.get('setting', ''))
    prompt = prompt.replace("{{THEME}}", config.get('theme', ''))
    prompt = prompt.replace("{{GLITCH_CONCEPT}}", config.get('glitch_concept', ''))
    prompt = prompt.replace("{{TIMELINE_LENGTH}}", str(config.get('timeline_length_weeks', 4)))

    output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="generate_storyline")
    
    if output:
        with open(timeline_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved timeline to {timeline_file}")

if __name__ == "__main__":
    main()
