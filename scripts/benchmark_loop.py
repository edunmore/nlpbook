#!/usr/bin/env python3
"""
Benchmark Loop Script

Automates the creation of a new world and runs the full generation pipeline
to verify system functionality and content quality.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

# Config
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WORLDS_DIR = WORKSPACE_ROOT / "worlds"
SCRIPTS_DIR = WORKSPACE_ROOT / "scripts"

BENCHMARK_WORLD = "benchmark-test"
MODEL = "gemini"

def run_cmd(cmd, description):
    print(f"\n--- {description} ---")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Success")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)

def main():
    print(f"Starting Benchmark Loop for world: {BENCHMARK_WORLD}")
    
    # 1. Clean previous run
    world_dir = WORLDS_DIR / BENCHMARK_WORLD
    if world_dir.exists():
        print(f"Cleaning up {world_dir}...")
        shutil.rmtree(world_dir)
    
    os.makedirs(world_dir / "canon", exist_ok=True)
    os.makedirs(world_dir / "chapters", exist_ok=True)
    
    # 2. Seed Config
    config = {
        "title": "The Echo of Silence",
        "protagonist": {
            "name": "Kaelen Thorne",
            "role": "Xeno-archaeologist",
            "age": 45,
            "signature": "Obsessive note-taking, gentle touch with artifacts",
            "flaw": "Prefers the dead to the living"
        },
        "setting": "An abandoned Dyson sphere, overgrown with biomechanical flora.",
        "theme": "The cost of knowing the truth.",
        "glitch_concept": "The flora hums a frequency that rewrites short-term memory.",
        "characters": [
            {
                 "name": "Kaelen Thorne",
                 "role": "Protagonist",
                 "description": "Xeno-archaeologist. Obsessive note-taking, gentle touch with artifacts. Prefers the dead to the living."
            }
        ],
        "timeline_length_weeks": 4
    }
    
    config_path = world_dir / "canon" / "world_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Created seed config at {config_path}")
    
    # 3. Generate Characters
    run_cmd(
        [sys.executable, str(SCRIPTS_DIR / "generate_characters.py"), "--world", BENCHMARK_WORLD, "--count", "3", "--model", MODEL],
        "Generating Characters"
    )
    
    # 4. Generate Storyline
    run_cmd(
        [sys.executable, str(SCRIPTS_DIR / "generate_storyline.py"), "--world", BENCHMARK_WORLD, "--model", MODEL],
        "Generating Storyline"
    )
    
    # 5. Generate Chapter 1
    run_cmd(
        [sys.executable, str(SCRIPTS_DIR / "generate_chapters.py"), "--world", BENCHMARK_WORLD, "--count", "1", "--start", "1", "--model", MODEL],
        "Generating Chapter 1"
    )
    
    # 6. Report
    print("\n--- Benchmark Results ---")
    
    # Show Characters
    with open(config_path, "r") as f:
        data = json.load(f)
        print(f"Characters ({len(data['characters'])}):")
        for c in data['characters']:
            print(f"- {c['name']} ({c['role']})")

    # Show Chapter Start
    chap1 = world_dir / "chapters" / "CH001-Generated.md"
    # Find the actual filename since generate_chapters might rename it
    files = list((world_dir / "chapters").glob("CH001-*.md"))
    if files:
        with open(files[0], "r") as f:
            content = f.read()
            print(f"\nChapter 1 Preview ({files[0].name}):")
            print("-" * 40)
            print(content[:500] + "...")
            print("-" * 40)
    else:
        print("❌ Chapter 1 file not found!")

if __name__ == "__main__":
    main()
