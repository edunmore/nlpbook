#!/usr/bin/env python3
"""
Evaluate Plan Script

Reads `TIMELINE.md` and all Chapter Cards, then self-critiques using `PLAN_EVALUATOR.md`.
"""

import argparse
import glob
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
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    if not world_dir.exists():
        print(f"World '{args.world}' not found")
        sys.exit(1)

    # Load Timeline
    timeline_path = world_dir / "canon" / "TIMELINE.md"
    timeline_content = load_file(timeline_path)
    if not timeline_content:
        print("Warning: TIMELINE.md not found or empty.")

    # Load All Chapter Cards
    cards_dir = world_dir / "planning" / "chapter-cards"
    cards_content = ""
    if cards_dir.exists():
        card_files = sorted(glob.glob(str(cards_dir / "CH*.md")))
        for f in card_files:
            cards_content += f"\n--- {Path(f).name} ---\n{load_file(f)}\n"
            
    if not cards_content:
        print("Warning: No chapter cards found.")
        
    # Load Template
    template = load_template(world_dir, "PLAN_EVALUATOR.md")
    if not template:
        print("Template PLAN_EVALUATOR.md not found.")
        sys.exit(1)

    # Inject
    prompt = template.replace("{{TIMELINE}}", timeline_content)
    prompt = prompt.replace("{{CHAPTER_CARDS}}", cards_content)
    
    # Run
    output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="evaluate_plan")
    
    if output:
        # Save Report
        planning_dir = world_dir / "planning"
        os.makedirs(planning_dir, exist_ok=True)
        report_path = planning_dir / "EVALUATION_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(output)
            
        print(f"Saved evaluation report to {report_path}")

if __name__ == "__main__":
    main()
