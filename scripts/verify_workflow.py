#!/usr/bin/env python3
import subprocess
import json
import os
from pathlib import Path
import time

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = WORKSPACE_ROOT / "scripts"
WORLDS_DIR = WORKSPACE_ROOT / "worlds"
TEST_WORLD = "workflow-verification-test"

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False, result.stderr
    return True, result.stdout

def main():
    print(f"--- Starting Workflow Verification for {TEST_WORLD} ---")
    
    # 1. Create World (via internal logic simulation or calling backend if running, 
    # but let's just trigger the creation logic directly if possible or use a manual setup)
    # For a headless script, we'll simulate what the backend does.
    
    world_dir = WORLDS_DIR / TEST_WORLD
    if world_dir.exists():
        import shutil
        shutil.rmtree(world_dir)
    
    # We'll use the CLI to test the scripts directly
    os.makedirs(world_dir / "canon", exist_ok=True)
    
    # Setup minimal config
    config = {
        "title": "Verification Quest",
        "theme": "Testing the system",
        "source_path": "NLP",
        "characters": [{"name": "Tester", "role": "Main", "description": "A script"}],
        "workflow_stage": "brainstorm"
    }
    with open(world_dir / "canon" / "world_config.json", "w") as f:
        json.dump(config, f)

    # 2. Run Brainstorming (Discovery + Extraction)
    print("\n[Step 2] Brainstorming...")
    success, output = run_cmd([
        "python3", str(SCRIPTS_DIR / "generate_brainstorm_iterative.py"),
        "--world", TEST_WORLD,
        "--max-files", "2"
    ])
    
    if not success or "Discovery complete" not in output:
        print("❌ Brainstorming Discovery failed or wasn't logged.")
        return

    # Check output file
    if not (world_dir / "planning" / "BRAINSTORM_RAW.json").exists():
        print("❌ BRAINSTORM_RAW.json not created.")
        return
    
    print("✅ Brainstorming successful.")

    # 3. Generate Chapter Map
    print("\n[Step 3] Chapter Map...")
    success, output = run_cmd([
        "python3", str(SCRIPTS_DIR / "generate_chapter_map.py"),
        "--world", TEST_WORLD,
        "--count", "3"
    ])
    
    if not success or not (world_dir / "planning" / "CHAPTER_MAP.md").exists():
        print("❌ Chapter Map generation failed.")
        return
    print("✅ Chapter Map created.")

    # 4. Generate Chapter Cards
    print("\n[Step 4] Chapter Cards...")
    success, output = run_cmd([
        "python3", str(SCRIPTS_DIR / "generate_chapter_cards.py"),
        "--world", TEST_WORLD,
        "--count", "1",
        "--start", "1"
    ])
    
    if not success or not (world_dir / "planning" / "chapter-cards" / "CH001.md").exists():
        print("❌ Chapter Card generation failed.")
        return
    print("✅ Chapter Card created.")

    # 5. Generate Chapters
    print("\n[Step 5] Chapters...")
    success, output = run_cmd([
        "python3", str(SCRIPTS_DIR / "generate_chapters.py"),
        "--world", TEST_WORLD,
        "--count", "1",
        "--start", "1"
    ])
    
    if not success or not (world_dir / "chapters" / "CH001.md").exists():
        print("❌ Chapter generation failed.")
        return
    print("✅ Chapter created.")

    print(f"\n--- Verification Complete: SUCCESS ---")

if __name__ == "__main__":
    main()
