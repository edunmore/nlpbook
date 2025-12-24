#!/usr/bin/env python3
"""
Build Foundations Script
Orchestrates the 4-Phase Agent Protocol (Genesis -> Psyche -> Embodiment -> Crucible)
to populate the 'canon/' directory.
"""

import argparse
import json
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
    except:
        return ""

def save_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {path.name}")

def parse_json_output(output):
    """Clean markdown code blocks and parse JSON."""
    try:
        clean = output.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return json.loads(clean)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw Output: {output}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", required=True, help="World name")
    parser.add_argument("--model", default="gemini", help="Model to use")
    parser.add_argument("--theme", default="Generic", help="Optional theme override")
    args = parser.parse_args()

    world_dir = WORLDS_DIR / args.world
    canon_dir = world_dir / "canon"
    
    # Ensure structure exists
    concept_dir = canon_dir / "01_CONCEPT"
    profile_dir = canon_dir / "02_CHARACTER_PROFILE"
    plot_dir = canon_dir / "03_PLOT_DYNAMICS"
    
    for d in [concept_dir, profile_dir, plot_dir]:
        os.makedirs(d, exist_ok=True)

    # 1. Load Inspiration
    inspiration_path = world_dir / "planning" / "INSPIRATION.md"
    inspiration_text = load_file(inspiration_path)
    if not inspiration_text:
        print("Warning: No INSPIRATION.md found. Using generic theme.")
        inspiration_text = f"Theme: {args.theme}"

    # --- PHASE 1: GENESIS ---
    print("\n--- Phase 1: Genesis Agent ---")
    genesis_prompt = load_prompt(world_dir, "AGENT_GENESIS.md")
    prompt = genesis_prompt.replace("{{SOURCE_MATERIAL}}", inspiration_text)
    prompt = prompt.replace("{{THEME}}", args.theme)
    
    out_gen = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="genesis_foundation")
    data_gen = parse_json_output(out_gen)
    
    if not data_gen: return

    save_file(concept_dir / "01_logline.md", data_gen['logline'])
    save_file(concept_dir / "02_core_identity.md", data_gen['core_identity'])
    # Save Arc as MD table
    arc = data_gen['arc']
    arc_md = f"| Initial State | Final State |\n|---|---|\n| {arc['initial_state']} | {arc['final_state']} |"
    save_file(concept_dir / "03_character_arc_summary.md", arc_md)


    # --- PHASE 2: PSYCHE ---
    print("\n--- Phase 2: Psyche Agent ---")
    psyche_prompt = load_prompt(world_dir, "AGENT_PSYCHE.md")
    prompt = psyche_prompt.replace("{{LOGLINE}}", data_gen['logline'])
    prompt = prompt.replace("{{CORE_IDENTITY}}", data_gen['core_identity'])
    prompt = prompt.replace("{{ARC_SUMMARY}}", arc_md)
    
    out_psy = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="psyche_foundation")
    data_psy = parse_json_output(out_psy)
    
    if not data_psy: return

    save_file(profile_dir / "01_backstory_ghost.md", data_psy['ghost'])
    
    goals_md = f"# Goals\n* External: {data_psy['goals']['external']}\n* Internal: {data_psy['goals']['internal']}\n* Motivation: {data_psy['goals']['motivation']}"
    save_file(profile_dir / "02_goals_and_motivations.md", goals_md)
    
    flaw_md = f"# Fatal Flaw: {data_psy['fatal_flaw']['flaw']}\n* Scenario: {data_psy['fatal_flaw']['scenario']}\n* Obstacle: {data_psy['fatal_flaw']['obstacle']}"
    save_file(profile_dir / "03_fatal_flaw_analysis.md", flaw_md)
    
    wv_md = "| Value | Impact |\n|---|---|\n"
    for item in data_psy['worldview']:
        wv_md += f"| {item['value']} | {item['impact']} |\n"
    save_file(profile_dir / "04_worldview_matrix.md", wv_md)


    # --- PHASE 3: EMBODIMENT ---
    print("\n--- Phase 3: Embodiment Agent ---")
    emb_prompt = load_prompt(world_dir, "AGENT_EMBODIMENT.md")
    prompt = emb_prompt.replace("{{CORE_IDENTITY}}", data_gen['core_identity'])
    prompt = prompt.replace("{{PSYCHE_JSON}}", json.dumps(data_psy, indent=2))
    
    out_emb = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="embodiment_foundation")
    data_emb = parse_json_output(out_emb)
    
    if not data_emb: return

    phys_md = f"# Physical\n{data_emb['physical']['appearance']}\n## Sensory\n* Sight: {data_emb['physical']['sight']}\n* Sound: {data_emb['physical']['sound']}\n* Smell: {data_emb['physical']['smell']}\n* Touch: {data_emb['physical']['touch']}"
    save_file(profile_dir / "05_physical_sensory_profile.md", phys_md)
    
    voice_md = f"# Voice Sample\n> {data_emb['voice']['sample']}\n\n## Analysis\n{data_emb['voice']['analysis']}"
    save_file(profile_dir / "06_dialogue_voice_sample.md", voice_md)
    
    quirk_md = f"* Quirk: {data_emb['quirks']['quirk']}\n* Hobby: {data_emb['quirks']['hobby']}\n* Coping: {data_emb['quirks']['coping']}"
    save_file(profile_dir / "07_quirks_and_habits.md", quirk_md)


    # --- PHASE 4: CRUCIBLE ---
    print("\n--- Phase 4: Crucible Agent ---")
    cruc_prompt = load_prompt(world_dir, "AGENT_CRUCIBLE.md")
    prompt = cruc_prompt.replace("{{CORE_IDENTITY}}", data_gen['core_identity'])
    prompt = prompt.replace("{{PSYCHE_JSON}}", json.dumps(data_psy, indent=2))
    prompt = prompt.replace("{{EMBODIMENT_JSON}}", json.dumps(data_emb, indent=2))
    
    out_cruc = run_agent(prompt, model=args.model, world_dir=world_dir, task_name="crucible_foundation")
    data_cruc = parse_json_output(out_cruc)
    
    if not data_cruc: return

    conf_md = f"# Conflicts\n* External: {data_cruc['conflicts']['external']}\n* Internal: {data_cruc['conflicts']['internal']}"
    save_file(plot_dir / "01_conflict_statement.md", conf_md)
    
    save_file(plot_dir / "02_stakes_assessment.md", data_cruc['stakes'])
    
    cast_md = f"* Ally: {data_cruc['cast']['ally']}\n* Antagonist: {data_cruc['cast']['antagonist']}\n* Foil: {data_cruc['cast']['foil']}"
    save_file(plot_dir / "03_cast_dossier.md", cast_md)
    
    save_file(plot_dir / "04_agency_midpoint_crisis.md", data_cruc['midpoint'])
    
    print("\nFoundation Build Complete. Canon populated.")

if __name__ == "__main__":
    main()
