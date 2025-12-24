#!/usr/bin/env python3
"""
Generate World Script

Holistic generation of world configuration (Setting, Theme, Glitch, Characters).
Reads `world_config.json`, applies "AI:" instructions, and updates the config in place.
"""

import argparse
import json
import os
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
    parser.add_argument("--world", default="NEWORLDTEMPLATE", help="World name")
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
    
    # Load Prompt Template
    template_name = "WORLD_BUILDER.md"
    template_path = world_dir / "prompts" / template_name
    
    if not template_path.exists():
         template_path = PROMPTS_DIR / template_name
         
    if not template_path.exists():
        print(f"Prompt template not found: {template_name}")
        sys.exit(1)
        
    print(f"Using Prompt Template: {template_path}")
    prompt_template = load_file(template_path)

    # Format Context
    chars_text = ""
    for char in config.get('characters', []):
        chars_text += f"- {char.get('name', 'Unknown')} ({char.get('role', 'Unknown')}): {char.get('description', '')}\n"
        if char.get('tags'):
            chars_text += f"  Tags: {', '.join(char['tags'])}\n"

    # Inject Context
    prompt = prompt_template.replace("{{TITLE}}", config.get('title', 'Unknown'))
    prompt = prompt.replace("{{SETTING}}", config.get('setting', ''))
    prompt = prompt.replace("{{THEME}}", config.get('theme', ''))
    prompt = prompt.replace("{{GLITCH}}", config.get('glitch_concept', ''))
    prompt = prompt.replace("{{CHARACTERS}}", chars_text)

    # Run Agent
    output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="generate_world", cwd=world_dir)
    
    if output:
        try:
            # Clean output
            clean_output = output.strip()
            if clean_output.startswith("```json"):
                clean_output = clean_output[7:]
            if clean_output.endswith("```"):
                clean_output = clean_output[:-3]
            
            new_data = json.loads(clean_output)
            
            # Merge / Update Config
            # We overwrite these fields if they exist in output
            if 'setting' in new_data:
                config['setting'] = new_data['setting']
            if 'theme' in new_data:
                config['theme'] = new_data['theme']
            if 'glitch_concept' in new_data:
                config['glitch_concept'] = new_data['glitch_concept']
            
            # For characters, we assume the agent returns the COMPLETE list including updates and new ones.
            # However, if the agent only returns new ones, we might lose data.
            # The prompt says: "Refine and expand... Return strictly a single valid JSON object... characters: [...]"
            # It implies the full list.
            if 'characters' in new_data and isinstance(new_data['characters'], list):
                config['characters'] = new_data['characters']

            save_json(config_path, config)
            print("World generation complete. Config updated.")
            
        except json.JSONDecodeError:
            print("Failed to parse agent output as JSON.")
            print("Output was:")
            print(output)
    else:
        print("Agent returned no output.")

if __name__ == "__main__":
    main()
