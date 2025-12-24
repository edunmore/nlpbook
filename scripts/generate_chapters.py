#!/usr/bin/env python3
"""
Generate Chapters (Recursive)
Implements the 'Story Engine' protocol:
1. Loads previous [STORY_STATE] context.
2. Injects 'Beat' from Chapter Card.
3. Generates Scene/Sequel.
4. Updates [STORY_STATE].
"""

import argparse
import glob
import re
import os
import sys
from pathlib import Path

# Add scripts dir
sys.path.append(str(Path(__file__).resolve().parent))
from agent_utils import run_agent, load_prompt

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def get_last_chapter_file(chapters_dir):
    files = sorted(glob.glob(str(chapters_dir / "CH*.md")))
    if not files:
        return None
    return files[-1]

def extract_story_state(content):
    """
    Extracts the ```story_state ... ``` block from the end of a file.
    """
    pattern = r"```story_state(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)
    if matches:
        return matches[-1].strip()
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", required=True, help="World name")
    parser.add_argument("--count", type=int, default=1, help="Chapters to generate")
    parser.add_argument("--start", type=int, default=1, help="Start chapter number")
    parser.add_argument("--model", default="gemini", help="Model to use")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    chapters_dir = world_dir / "chapters"
    cards_dir = world_dir / "planning" / "chapter-cards"
    
    os.makedirs(chapters_dir, exist_ok=True)

    # Load Template
    # We use WRITER_SCENE_SEQUEL.md by default now
    writer_prompt = load_prompt(world_dir, "WRITER_SCENE_SEQUEL.md")
    if not writer_prompt:
        print("Error: WRITER_SCENE_SEQUEL.md not found.")
        sys.exit(1)

    # Main Loop
    current_chap = args.start
    for _ in range(args.count):
        chap_str = f"{current_chap:03}"
        print(f"\nGeneraring CH{chap_str}...")

        # 1. Context: Previous Story State
        previous_state = ""
        last_file_path = get_last_chapter_file(chapters_dir)
        
        if last_file_path:
            content = load_file(last_file_path)
            state_block = extract_story_state(content)
            if state_block:
                previous_state = f"```story_state\n{state_block}\n```"
                print("  -> Loaded [STORY_STATE] from previous chapter.")
            else:
                print("  -> Warning: No [STORY_STATE] found in previous chapter.")
        else:
            print("  -> First chapter. Starting fresh.")
            # Could inject init state from canon if needed?

        # 2. Context: Chapter Card (Beat)
        card_path = cards_dir / f"CH{chap_str}.md"
        beat_description = ""
        if card_path.exists():
            beat_description = load_file(card_path)
            print(f"  -> Loaded Beat: {card_path.name}")
        else:
            print(f"  -> Warning: No chapter card found for CH{chap_str}")
            beat_description = "Write the next logical chapter focusing on character conflict."

        # 3. Context: Previous Content (Last ~1000 chars for continuity)
        prior_context = ""
        if last_file_path:
             content = load_file(last_file_path)
             # simple truncation
             prior_context = content[-2000:] if len(content) > 2000 else content

        # 4. Construct Prompt
        # Our template: {{CHAPTER_NUM}}, {{PREVIOUS_CONTENT}}, {{BEAT_DESCRIPTION}}, {{INSTRUCTIONS}}
        
        # We inject the STORY STATE into 'PREVIOUS_CONTENT' or a new variable?
        # The prompt template has {{PREVIOUS_CONTENT}}. Let's combine them.
        
        full_prior = f"**Last Chapter Excerpt**:\n{prior_context}\n\n**Current State**:\n{previous_state}"
        
        prompt = writer_prompt.replace("{{CHAPTER_NUM}}", chap_str)
        prompt = prompt.replace("{{PREVIOUS_CONTENT}}", full_prior)
        prompt = prompt.replace("{{BEAT_DESCRIPTION}}", beat_description)
        prompt = prompt.replace("{{INSTRUCTIONS}}", "Focus on the 'Ghost' and 'Lie'.")

        # 5. Run Agent
        output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name=f"write_ch{chap_str}", cwd=world_dir)
        
        if output:
            out_file = chapters_dir / f"CH{chap_str}.md"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"  -> Saved {out_file.name}")
        
        current_chap += 1

if __name__ == "__main__":
    main()
