#!/usr/bin/env python3
"""
Generate Chapter Map Script

Creates planning/CHAPTER_MAP.md from approved brainstorm concepts.
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from agent_utils import run_agent

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"
PROMPTS_DIR = WORKSPACE_ROOT / "prompts"

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def load_template(world_dir, filename):
    world_prompt = world_dir / "prompts" / filename
    if world_prompt.exists():
        return load_file(world_prompt)
    global_prompt = PROMPTS_DIR / filename
    if global_prompt.exists():
        return load_file(global_prompt)
    return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini", help="CLI tool to use")
    parser.add_argument("--world", default="default", help="World name")
    parser.add_argument("--count", type=int, default=10, help="Number of chapters")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    if not world_dir.exists():
        print(f"World '{args.world}' not found")
        sys.exit(1)

    config_path = world_dir / "canon" / "world_config.json"
    config = load_json(config_path)
    
    # Load approved concepts
    brainstorm_path = world_dir / "planning" / "BRAINSTORM_RAW.json"
    if not brainstorm_path.exists():
        print("No brainstorm found. Run generate_brainstorm_iterative.py first.")
        sys.exit(1)
    
    all_concepts = load_json(brainstorm_path)
    
    # Filter to approved/high-rated concepts
    approved = [c for c in all_concepts if c.get('approved') or c.get('rating', 0) >= 3]
    if not approved:
        # If nothing explicitly approved, use all with rating > 0
        approved = [c for c in all_concepts if c.get('rating', 0) > 0]
    if not approved:
        # Fallback to all concepts
        approved = all_concepts
        
    print(f"Using {len(approved)} approved concepts")
    
    # Format concepts for prompt
    concepts_text = ""
    for idx, c in enumerate(approved):
        concepts_text += f"{idx+1}. **{c.get('concept', 'Unknown')}**\n"
        concepts_text += f"   - {c.get('description', '')}\n"
        concepts_text += f"   - Scene idea: {c.get('scene_idea', '')}\n\n"
    
    # Prepare characters
    chars_text = ""
    for char in config.get('characters', []):
        chars_text += f"- {char['name']} ({char['role']}): {char.get('description', '')}\n"
    
    # Load template
    template = load_template(world_dir, "CHAPTER_MAP_GENERATOR.md")
    if not template:
        print("Template CHAPTER_MAP_GENERATOR.md not found.")
        sys.exit(1)
    
    prompt = template
    prompt = prompt.replace("{{TITLE}}", config.get('title', 'Unknown'))
    prompt = prompt.replace("{{THEME}}", config.get('theme', ''))
    prompt = prompt.replace("{{SETTING}}", config.get('setting', ''))
    prompt = prompt.replace("{{CHARACTERS}}", chars_text)
    prompt = prompt.replace("{{CONCEPTS}}", concepts_text)
    prompt = prompt.replace("{{CHAPTER_COUNT}}", str(args.count))
    
    output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="generate_chapter_map")
    
    if output:
        planning_dir = world_dir / "planning"
        os.makedirs(planning_dir, exist_ok=True)
        map_path = planning_dir / "CHAPTER_MAP.md"
        
        with open(map_path, "w", encoding="utf-8") as f:
            f.write(output)
            
        print(f"Saved chapter map to {map_path}")
        
        # Update workflow stage
        config['workflow_stage'] = 'map_review'
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()
