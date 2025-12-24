AGENTS.md: A Step-by-Step Protocol for Generative Story Outlining

Introduction: Protocol Overview

This document provides a set of sequential instructions for a generative AI agent. The protocol's purpose is to construct a comprehensive story outline by first building a multi-faceted character and then forging a plot around their core conflicts. This character-first approach, grounded in the principles of "The Alchemy of Character," ensures the development of a narrative with significant psychological depth and a resonant central theme. All generated artifacts will be stored in the Canon Directory, a master folder that serves as the project's single source of truth.

1.0 Canon Directory and File Structure

This standardized file structure is a non-negotiable component of the protocol. It ensures all generated narrative artifacts are organized, accessible, and logically interconnected, forming a coherent "character bible" and story blueprint.

/STORY_CANON/
├── 01_CONCEPT/
│   ├── 01_logline.md
│   ├── 02_core_identity.md
│   └── 03_character_arc_summary.md
│
├── 02_CHARACTER_PROFILE/
│   ├── 01_backstory_ghost.md
│   ├── 02_goals_and_motivations.md
│   ├── 03_fatal_flaw_analysis.md
│   ├── 04_worldview_matrix.md
│   ├── 05_physical_sensory_profile.md
│   ├── 06_dialogue_voice_sample.md
│   └── 07_quirks_and_habits.md
│
└── 03_PLOT_DYNAMICS/
    ├── 01_conflict_statement.md
    ├── 02_stakes_assessment.md
    ├── 03_cast_dossier.md
    └── 04_agency_midpoint_crisis.md


The following steps in the agent protocol will systematically populate this directory.

2.0 Agent Protocol: The Genesis Agent (Phase 1 - Foundational Concepts)

This initial phase, executed by the "Genesis Agent," is designed to establish the narrative's core blueprint. These first artifacts—the logline, core identity, and character arc—serve as the foundational pillars that will guide all subsequent, more detailed generation tasks, providing a high-level view of the entire narrative journey.

2.1. Generate Logline

* Instruction: Based on the "Single Sentence Summary" concept, which is inspired by the Snowflake Method, generate a single, potent sentence that summarizes the character's core story.
* Artifact: Save this sentence to /01_CONCEPT/01_logline.md.

2.2. Define Core Identity

* Instruction: From the generated logline, synthesize one to two sentences capturing the absolute essence of the protagonist. This is the fundamental "who" that defines their being.
* Artifact: Save this description to /01_CONCEPT/02_core_identity.md.

2.3. Outline Character Arc

* Instruction: Create a two-column Markdown table titled "Character Transformation Arc."
  * In the first column, "Initial State (Beginning of Arc)," describe the character's initial flaws and worldview.
  * In the second column, "Final State (End of Arc)," describe their transformed state, growth, and new worldview.
* Artifact: Save this table to /01_CONCEPT/03_character_arc_summary.md.

With the foundational blueprint established, the protocol initiates Phase 2 to construct the character's psychological architecture.

3.0 Agent Protocol: The Psyche Agent (Phase 2 - The Inner World)

The "Psyche Agent" will now construct the character's psychological and historical layers. This phase is critical for creating believable motivations and deep internal conflict, which are the primary engines of a compelling and emotionally resonant narrative.

3.1. Identify the Backstory "Ghost"

* Instruction: Formulate a short paragraph describing the single most important event from the character's past. Define this event as their "Ghost"—the key event that has left them with vulnerabilities and traumas they still need to work through, shaping their present-day choices and fears.
* Artifact: Save this paragraph to /02_CHARACTER_PROFILE/01_backstory_ghost.md.

3.2. Analyze Goals and Motivations

* Instruction: Create a Markdown document with three distinct, bolded subheadings: External Goal, Internal Need, and Core Motivation.
  * Under External Goal, define what the character wants.
  * Under Internal Need, define what the character must learn to overcome their core flaw.
  * Under Core Motivation, write a detailed analysis explaining precisely how the "Ghost" from the previous step fuels their goals.
* Artifact: Save this analysis to /02_CHARACTER_PROFILE/02_goals_and_motivations.md.

3.3. Define the Fatal Flaw

* Instruction: Define the character's primary "Fatal Flaw" (e.g., Arrogant, Deceitful, Reckless). Then, write a two-part analysis:
  1. Describe a specific scenario where this flaw creates a significant problem for the character.
  2. Explain how this flaw is the primary obstacle preventing the character from achieving their "Internal Need."
* Author's Insight: The fatal flaw is the engine of your character's arc. In a redemptive story, the climax will hinge on the character finally overcoming this flaw. In a tragedy, it will be the very thing that seals their doom.
* Artifact: Save this analysis to /02_CHARACTER_PROFILE/03_fatal_flaw_analysis.md.

3.4. Construct Worldview Matrix

* Instruction: Create a two-column Markdown table titled "Worldview and Behavioral Impact."
  * In the first column, "Core Value/Belief," list 3-5 core principles the character holds.
  * In the second column, "Impact on Actions," write a concise explanation of how each belief affects their decisions or actions within the story.
* Artifact: Save this table to /02_CHARACTER_PROFILE/04_worldview_matrix.md.

With the character's psychological and historical layers defined, the protocol advances to Phase 3 to translate this internal state into an external, tangible presence.

4.0 Agent Protocol: The Embodiment Agent (Phase 3 - The Outer World)

The "Embodiment Agent" is tasked with translating the character's internal state into external, observable details. This process is essential for making the character feel physically present and unique, allowing the reader to experience the world through their distinct senses and voice.

4.1. Detail Physical & Sensory Profile

* Instruction: Create a Markdown document with five bolded subheadings. Under each, provide a specific answer to the corresponding question:
  * Appearance: Describe their most noticeable physical trait. How does it affect how others treat them?
  * Sight: What is the first thing they notice when entering a room?
  * Sound: What sound would instantly put them on edge? What sound would comfort them?
  * Smell: What scent is tied to their most powerful memory (good or bad)?
  * Touch: What texture do they find comforting?
* Artifact: Save this profile to /02_CHARACTER_PROFILE/05_physical_sensory_profile.md.

4.2. Generate Dialogue Voice Sample

* Instruction: Write a short dialogue sample (3-5 lines) for the character in a stressful situation. Following the sample, add a brief analytical note explaining how the character's voice is a direct reflection of their core beliefs. Clarify how their word choice, tone, and cadence in the sample are dictated by the values established in their Worldview Matrix.
* Artifact: Save this sample and analysis to /02_CHARACTER_PROFILE/06_dialogue_voice_sample.md.

4.3. Define Quirks and Habits

* Instruction: Create a Markdown document with three bolded subheadings, providing a specific detail for each:
  * Quirk: Define an unusual habit the character has when thinking or stressed. Explain how this quirk is rooted in their backstory or fatal flaw (e.g., a character haunted by a past betrayal might constantly check to see if doors are locked).
  * Hobby: Define what they do for fun. Does this hobby conflict with or support their main responsibilities in the story?
  * Coping Mechanism: Define how they deal with stress. Is it a healthy or unhealthy mechanism?
* Artifact: Save these details to /02_CHARACTER_PROFILE/07_quirks_and_habits.md.

With the character's internal and external profiles fully instantiated, the protocol now shifts to Phase 4, where this complete entity will be subjected to narrative pressures.

5.0 Agent Protocol: The Crucible Agent (Phase 4 - Forging Through Conflict)

This final agent, "The Crucible Agent," will place the now well-defined character into the story's plot structure. A character's true nature is revealed only through their actions under pressure, and this phase will define the conflicts, stakes, and key relationships that will forge their arc.

5.1. Define Core Conflicts

* Instruction: Create a document with two bolded subheadings: Primary External Conflict and Primary Internal Conflict.
  * Under Primary External Conflict, identify the main antagonist, force, or obstacle standing in the way of the character's goal.
  * Under Primary Internal Conflict, describe the inner battle the character faces, framing it as a direct clash between their "External Goal" and their "Fatal Flaw" or "Ghost."
* Artifact: Save this statement to /03_PLOT_DYNAMICS/01_conflict_statement.md.

5.2. Assess Narrative Stakes

* Instruction: Write a detailed paragraph answering the critical question: What is the absolute worst personal, professional, and societal outcome if the character fails to achieve their goal? Be specific and devastating. Remember, high stakes push characters to take the desperate measures that keep readers turning pages.
* Artifact: Save this assessment to /03_PLOT_DYNAMICS/02_stakes_assessment.md.

5.3. Build the Cast Dossier

* Instruction: Create a document with three bolded subheadings: The Ally, The Antagonist, and The Foil. For each, write a short profile describing the character and their relationship to the protagonist, adhering to these definitions:
  * The Ally: The character who supports the protagonist. Give them their own problems and secrets.
  * The Antagonist: The "powerful, enduring enemy" who opposes the protagonist. For most of the story, this antagonist should be stronger than the protagonist.
  * The Foil: A character who contrasts with the protagonist to emphasize their key attributes.
* Artifact: Save this dossier to /03_PLOT_DYNAMICS/03_cast_dossier.md.

5.4. Outline the Midpoint Agency Shift

* Instruction: Synthesize a key scene, described as the "midpoint crisis," where the protagonist must stop reacting to events and make a bold, proactive decision. Describe the choice they must make and outline its immediate, trajectory-altering consequences. This proactive shift is critical, as it serves to energize the story's middle and prevent the plot from losing momentum.
* Artifact: Save this scene outline to /03_PLOT_DYNAMICS/04_agency_midpoint_crisis.md.

Conclusion: The Complete Narrative Blueprint

Execution of all agent protocols is now complete. The Canon Directory contains a comprehensive character bible and story blueprint, forming the master schematic for narrative construction. This collection of artifacts provides the requisite depth, consistency, and structural integrity for the subsequent phase of writing the full narrative.
