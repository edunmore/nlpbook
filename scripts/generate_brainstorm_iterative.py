#!/usr/bin/env python3
"""
Iterative Brainstorm Script

Loops through source files one-by-one, extracting story concepts.
Outputs planning/BRAINSTORM_RAW.json for GUI review.
"""

import argparse
import json
import os
import sys
import glob
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from agent_utils import run_agent, load_prompt

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini", help="CLI tool to use")
    parser.add_argument("--world", default="NEWORLDTEMPLATE", help="World name")
    parser.add_argument("--max-files", type=int, default=10, help="Max source files to process")
    parser.add_argument("--chars-per-file", type=int, default=4000, help="Max chars to read per file")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    if not world_dir.exists():
        print(f"World '{args.world}' not found")
        sys.exit(1)

    config_path = world_dir / "canon" / "world_config.json"
    config = load_json(config_path)
    
    # Get source path
    source_path_str = config.get("source_path", "")
    if not source_path_str:
        source_dir = world_dir / "source"
    else:
        if source_path_str.startswith("/"):
            source_dir = Path(source_path_str)
        else:
            source_dir = WORKSPACE_ROOT / source_path_str
            
    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        sys.exit(1)
        
    # Get source files
    source_files = sorted(glob.glob(str(source_dir / "*.txt")) + glob.glob(str(source_dir / "*.md")))
    if not source_files:
        print(f"No source files found in {source_dir}")
        sys.exit(1)
        
    print(f"Found {len(source_files)} source files. Starting discovery scan...")
    
    # --- PHASE 1: DISCOVERY ---
    discovery_template = load_prompt(world_dir, "BRAINSTORM_DISCOVERY.md")
    if discovery_template:
        excerpts = ""
        for fpath in source_files:
            content = load_file(fpath)[:1000] # Small snippet for discovery
            excerpts += f"--- FILE: {Path(fpath).name} ---\n{content}\n\n"
        
        disc_prompt = discovery_template.replace("{{TITLE}}", config.get('title', 'Unknown'))
        disc_prompt = disc_prompt.replace("{{THEME}}", config.get('theme', ''))
        disc_prompt = disc_prompt.replace("{{SETTING}}", config.get('setting', ''))
        disc_prompt = disc_prompt.replace("{{EXCERPTS}}", excerpts)
        disc_prompt = disc_prompt.replace("{{COUNT}}", str(args.max_files))
        
        disc_output = run_agent(disc_prompt, model=args.model, world_dir=world_dir, task_name="brainstorm_discovery", cwd=world_dir)
        
        if disc_output:
            try:
                clean_disc = disc_output.strip()
                if clean_disc.startswith("```json"): clean_disc = clean_disc[7:]
                if clean_disc.endswith("```"): clean_disc = clean_disc[:-3]
                
                ranked_files = json.loads(clean_disc)
                prioritized_paths = []
                for rf in ranked_files:
                    target = next((p for p in source_files if Path(p).name == rf['filename']), None)
                    if target:
                        prioritized_paths.append(target)
                
                if prioritized_paths:
                    print(f"Discovery complete. Prioritized {len(prioritized_paths)} files.")
                    source_files = prioritized_paths
            except Exception as e:
                print(f"Warning: Discovery parsing failed: {e}. Falling back to default order.")
                source_files = source_files[:args.max_files]
    else:
        print("Warning: BRAINSTORM_DISCOVERY.md not found. Skipping discovery phase.")
        source_files = source_files[:args.max_files]

    # --- PHASE 2: EXTRACTION ---
    # Load template
    template = load_template(world_dir, "BRAINSTORM_ITERATIVE.md")
    if not template:
        print("Template BRAINSTORM_ITERATIVE.md not found.")
        sys.exit(1)
    
    # Prepare context
    chars_text = ""
    for char in config.get('characters', []):
        chars_text += f"- {char['name']} ({char['role']}): {char.get('description', '')}\n"
    
    all_concepts = []
    
    # Process each file
    for idx, fpath in enumerate(source_files):
        filename = Path(fpath).name
        print(f"\n[{idx+1}/{len(source_files)}] Processing: {filename}")
        
        content = load_file(fpath)[:args.chars_per_file]
        
        prompt = template
        prompt = prompt.replace("{{SOURCE_FILE}}", filename)
        prompt = prompt.replace("{{SOURCE_CONTENT}}", content)
        prompt = prompt.replace("{{TITLE}}", config.get('title', 'Unknown'))
        prompt = prompt.replace("{{THEME}}", config.get('theme', ''))
        prompt = prompt.replace("{{SETTING}}", config.get('setting', ''))
        
        output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name=f"brainstorm_{filename[:20]}", cwd=world_dir)
        
        if output:
            try:
                clean = output.strip()
                if clean.startswith("```json"):
                    clean = clean[7:]
                if clean.startswith("```"):
                    clean = clean[3:]
                if clean.endswith("```"):
                    clean = clean[:-3]
                
                concepts = json.loads(clean)
                for c in concepts:
                    # Deduplication check
                    if any(c['concept'].lower() == existing['concept'].lower() for existing in all_concepts):
                        continue
                        
                    c['source_file'] = filename
                    c['rating'] = 0  # For GUI review
                    c['approved'] = False
                    all_concepts.append(c)
                    
                print(f"  Extracted {len(concepts)} concepts")
            except json.JSONDecodeError:
                print(f"  Warning: Failed to parse JSON from {filename}")
    
    # Save results
    planning_dir = world_dir / "planning"
    os.makedirs(planning_dir, exist_ok=True)
    output_path = planning_dir / "BRAINSTORM_RAW.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2)
    
    print(f"\nSaved {len(all_concepts)} concepts to {output_path}")
    print("Use the GUI to review, rate, and approve concepts.")
    
    # Update workflow stage
    config['workflow_stage'] = 'brainstorm_review'
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()
