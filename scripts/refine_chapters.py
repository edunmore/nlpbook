#!/usr/bin/env python3
"""
Refine Chapters Script

Iterates over chapters in `chapters/`, applies improvement ideas using the agent CLI,
and saves the result to `chapters/refined/`.
"""

import argparse
import glob
import os
import subprocess
import sys
from pathlib import Path

# Add scripts dir to python path to import agent_utils
sys.path.append(str(Path(__file__).resolve().parent))
from agent_utils import run_agent

# Configuration
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"
PROMPTS_DIR = WORKSPACE_ROOT / "prompts"
IMPROVEMENT_FILE = PROMPTS_DIR / "IMPROVEMENT_IDEAS.md"
TEMPLATE_FILE = PROMPTS_DIR / "REFINE_CHAPTER.md"

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
        sys.exit(1)

def save_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {path}")

def get_chapters(chapters_dir, filter_chapter=None):
    # Pattern to match CH001... etc.
    pattern = str(chapters_dir / "CH*.md")
    files = sorted(glob.glob(pattern))
    
    if filter_chapter:
        files = [f for f in files if filter_chapter in Path(f).name]
        
    return files

def construct_prompt(chapter_content, improvement_ideas, chapter_num):
    template = load_file(TEMPLATE_FILE)
    prompt = template.replace("{{CHAPTER_CONTENT}}", chapter_content)
    # prompt = template.replace("{{CHAPTER_CONTENT}}", chapter_content) # Removed duplicate call
    prompt = prompt.replace("{{IMPROVEMENT_IDEAS}}", improvement_ideas)
    prompt = prompt.replace("{{CHAPTER_NUM}}", chapter_num)
    return prompt

def main():
    parser = argparse.ArgumentParser(description="Refine chapters using AI agent")
    parser.add_argument("--model", default="gemini", help="CLI tool to use (gemini or qwen)")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt instead of running agent")
    parser.add_argument("--chapter", help="Specific chapter number/string to filter (e.g. '001')")
    parser.add_argument("--world", default="NEWORLDTEMPLATE", help="World name")
    
    args = parser.parse_args()

    # Paths
    world_dir = WORLDS_DIR / args.world
    chapters_dir = world_dir / "chapters"
    refined_dir = chapters_dir / "refined"
    
    if not chapters_dir.exists():
        print(f"Chapters directory not found for world '{args.world}'")
        sys.exit(1)

    # Load instructions based on type
    instructions = ""
    if args.type.lower() == "custom":
        instructions = load_file(IMPROVEMENT_FILE)
    else:
        type_map = {
            "writer": "WRITER_INSTRUCTIONS.md",
            "cc": "CC_INSTRUCTIONS.md",
            "se": "SE_INSTRUCTIONS.md",
            "qa": "QA_INSTRUCTIONS.md",
            "po": "PO_INSTRUCTIONS.md"
        }
        target_file = type_map.get(args.type.lower())
        if target_file and (PROMPTS_DIR / target_file).exists():
            print(f"Loading system instructions: {target_file}")
            instructions = load_file(PROMPTS_DIR / target_file)
        else:
            print(f"Warning: Instruction file for '{args.type}' not found or unknown. Using custom improvement ideas.")
            instructions = load_file(IMPROVEMENT_FILE)

    if not instructions.strip():
        print(f"Warning: Instructions are empty.")

    # Get chapters
    chapters = get_chapters(chapters_dir, args.chapter)
    
    if not chapters:
        print("No chapters found matching criteria.")
        return

    print(f"Found {len(chapters)} chapters to process in '{args.world}'...")
    
    # Process loop
    for chapter_path in chapters:
        chapter_path_obj = Path(chapter_path)
        chapter_name = chapter_path_obj.name
        print(f"\nProcessing {chapter_name}...")
        
        # Extract number
        chapter_num = chapter_name.split("-")[0].replace("CH", "")
        
        # Check for specific feedback file
        feedback_file = chapters_dir / "meta" / f"{chapter_name}.feedback.md"
        local_feedback = ""
        if feedback_file.exists():
            print(f"  Found local feedback: {feedback_file}")
            local_feedback = load_file(feedback_file)
            
        # Combine instructions
        # Force rewrite instruction to override any "Report" requests in system prompts
        force_rewrite = "\n\nIMPORTANT: Ignore any requests for reports, logs, or analysis in the instructions above. Your goal is to REWRITE the chapter content applying these principles. Output ONLY the refined chapter markdown."
        
        full_instructions = instructions + force_rewrite
        if local_feedback.strip():
            full_instructions += "\n\n# Chapter Specific User Feedback\n" + local_feedback
        
        # Read content
        content = load_file(chapter_path)
        
        # Construct prompt
        prompt = construct_prompt(content, full_instructions, chapter_num)
        
        # Run agent
        task_name = f"refine_{chapter_name.replace('.md', '')}"
        
        if args.dry_run:
             print("\n--- DRY RUN PROMPT START ---")
             print(prompt)
             print("--- DRY RUN PROMPT END ---\n")
             output = "DRY RUN OUTPUT"
        else:
            output = run_agent(prompt, model=args.model, world_dir=world_dir, task_name=task_name, cwd=world_dir)
        
        if output and not args.dry_run:
            # Save output
            output_path = refined_dir / chapter_name
            save_file(output_path, output)

if __name__ == "__main__":
    main()
