#!/usr/bin/env python3
"""
Generate Chapter Cards Script

Generates planning/chapter-cards/CHxxx.md based on TIMELINE.md and world_config.
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

def load_file(path):
    try:
        if not path.exists(): return ""
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

def load_template(world_dir, filename):
    # 1. World Override
    world_prompt = world_dir / "prompts" / filename
    if world_prompt.exists():
        return load_file(world_prompt)
    
    # 2. Global Default
    global_prompt = WORKSPACE_ROOT / "prompts" / filename
    if global_prompt.exists():
        return load_file(global_prompt)
        
    return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini", help="CLI tool to use")
    parser.add_argument("--count", type=int, default=5, help="Number of cards to generate")
    parser.add_argument("--start", type=int, default=1, help="Start chapter number")
    parser.add_argument("--world", default="default", help="World name")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    if not world_dir.exists():
        print(f"World '{args.world}' not found")
        sys.exit(1)

    canon_dir = world_dir / "canon"
    planning_dir = world_dir / "planning"
    cards_dir = planning_dir / "chapter-cards"
    os.makedirs(cards_dir, exist_ok=True)
    
    config_file = canon_dir / "world_config.json"
    timeline_file = canon_dir / "TIMELINE.md"
    brainstorm_file = planning_dir / "BRAINSTORM.json"

    if not config_file.exists():
        print("Config not found")
        sys.exit(1)

    config = load_json(config_file)
    timeline = load_file(timeline_file)
    
    # Load Brainstorm if exists
    brainstorm_content = ""
    if brainstorm_file.exists():
        try:
            with open(brainstorm_file, "r", encoding="utf-8") as f:
                bs_data = json.load(f)
                brainstorm_content = "\n# Available Brainstorm Topics\n"
                for idx, item in enumerate(bs_data):
                    brainstorm_content += f"{idx+1}. **{item.get('title')}**\n"
                    brainstorm_content += f"   - Source: {item.get('source_concept')}\n"
                    brainstorm_content += f"   - Plot Idea: {item.get('plot_beat')}\n"
        except Exception as e:
            print(f"Warning: Failed to load BRAINSTORM.json: {e}")

    chars_text = ""
    for char in config.get('characters', []):
        chars_text += f"- **{char['name']}** ({char['role']}): {char.get('description', '')}\n"

    print(f"Generating {args.count} Chapter Cards for world '{args.world}'...")
    
    template_content = load_template(world_dir, "GENERATE_CARD.md")
    if not template_content:
        print("Error: Could not find GENERATE_CARD.md template.")
        sys.exit(1)

    for i in range(args.start, args.start + args.count):
        chap_num = f"{i:03}"
        print(f"Planning CH{chap_num}...")
        
        prompt = template_content
        prompt = prompt.replace("{{CHAPTER_NUM}}", chap_num)
        prompt = prompt.replace("{{TITLE}}", config.get('title', 'Unknown'))
        prompt = prompt.replace("{{THEME}}", config.get('theme', 'Unknown'))
        prompt = prompt.replace("{{SETTING}}", config.get('setting', 'Unknown'))
        prompt = prompt.replace("{{GLITCH}}", config.get('glitch_concept', 'Unknown'))
        prompt = prompt.replace("{{TIMELINE}}", timeline)
        prompt = prompt.replace("{{CHARACTERS}}", chars_text)
        
        # Inject Brainstorm if placeholder exists, else append
        if "{{BRAINSTORM}}" in prompt:
            prompt = prompt.replace("{{BRAINSTORM}}", brainstorm_content)
        else:
            prompt += f"\n\n{brainstorm_content}"
        
        output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name=f"plan_chapter_{chap_num}")
        
        if output:
            filename = f"CH{chap_num}.md"
            path = cards_dir / filename
            with open(path, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Saved {filename}")

if __name__ == "__main__":
    main()
