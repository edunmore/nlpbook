#!/usr/bin/env python3
"""
Analyze Source Script
Scans 'source/' directory and generates 'planning/INSPIRATION.md' using AGENT_ANALYZER.
"""

import argparse
import glob
import os
import sys
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
    planning_dir = world_dir / "planning"
    os.makedirs(planning_dir, exist_ok=True)

    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        return

    # Gather source files
    source_files = sorted(glob.glob(str(source_dir / "*.md"))) + sorted(glob.glob(str(source_dir / "*.txt")))
    
    if not source_files:
        print("No source files found.")
        return

    print(f"Found {len(source_files)} source files.")

    # Load Analyzer Prompt
    prompt_template = load_prompt(world_dir, "AGENT_ANALYZER.md")
    if not prompt_template:
        print("AGENT_ANALYZER.md not found.")
        sys.exit(1)

    aggregated_inspiration = "# INSPIRATION & DISCOVERY\n\n"

    for src_file in source_files:
        print(f"Analyzing {Path(src_file).name}...")
        content = load_file(src_file)
        
        # Construct Prompt
        # simple injection since AGENT_ANALYZER doesn't use {{VARS}} except context
        prompt = f"{prompt_template}\n\n# SOURCE MATERIAL\n{content}"
        
        output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name=f"analyze_{Path(src_file).stem}", cwd=world_dir)
        
        if output:
            aggregated_inspiration += f"## Source: {Path(src_file).name}\n{output}\n\n---\n\n"

    # Save Result
    out_path = planning_dir / "INSPIRATION.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(aggregated_inspiration)
    
    print(f"Analysis complete. Saved to {out_path}")

if __name__ == "__main__":
    main()
