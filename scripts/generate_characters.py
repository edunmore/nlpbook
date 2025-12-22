#!/usr/bin/env python3
"""
Generate Characters Script

Reads `world_config.json`, prompts agent for new characters, and appends them.
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

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Updated config: {path}")
    except Exception as e:
        print(f"Error saving {path}: {e}")

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini", help="CLI tool to use")
    parser.add_argument("--world", default="default", help="World name")
    parser.add_argument("--count", type=int, default=3, help="Number of characters to generate")
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
    
    # Select Trigger (Steering File)
    trigger_name = "CHARACTER_GENERATOR.md"
    trigger_path = world_dir / "prompts" / trigger_name
    
    if not trigger_path.exists():
         trigger_path = PROMPTS_DIR / trigger_name
         
    if not trigger_path.exists():
        print(f"Prompt template not found: {trigger_name}")
        sys.exit(1)
        
    print(f"Using Prompt Template: {trigger_path}")
    prompt_template = load_file(trigger_path)

    # Context
    existing_chars = config.get('characters', [])
    chars_text = ""
    for char in existing_chars:
        chars_text += f"- {char['name']} ({char['role']}): {char.get('description', '')}\n"

    # Inject Context
    prompt = prompt_template.replace("{{TITLE}}", config.get('title', 'Unknown'))
    prompt = prompt.replace("{{SETTING}}", config.get('setting', ''))
    prompt = prompt.replace("{{THEME}}", config.get('theme', ''))
    prompt = prompt.replace("{{EXISTING_CHARACTERS}}", chars_text)
    prompt = prompt.replace("{{COUNT}}", str(args.count))

    output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="generate_characters")
    
    if output:
        try:
            # Clean output if it contains markdown code blocks
            clean_output = output.strip()
            if clean_output.startswith("```json"):
                clean_output = clean_output[7:]
            if clean_output.endswith("```"):
                clean_output = clean_output[:-3]
            
            new_chars = json.loads(clean_output)
            
            if isinstance(new_chars, list):
                print(f"Generated {len(new_chars)} new characters.")
                for c in new_chars:
                    print(f"+ {c.get('name')} ({c.get('role')})")
                
                # Append
                config['characters'].extend(new_chars)
                save_json(config_path, config)
            else:
                print("Agent returned invalid JSON format (not a list).")
                print(output)
                
        except json.JSONDecodeError:
            print("Failed to parse agent output as JSON.")
            print("Output was:")
            print(output)

if __name__ == "__main__":
    main()
