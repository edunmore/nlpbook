# Technical Workflow Guide
This document details the exact file operations, prompt templates, and scripts used by each stage of the BookAgent workflow. It is the technical source of truth.

## 1. World Generation
**Goal**: Initialize a new world with context (Setting, Theme, Characters).

- **GUI Action**: "Auto-Generate (AI)" button on World Config page.
- **API Endpoint**: `/api/generate/world`
- **Script**: `scripts/generate_world.py`
- **Context**: `cwd = worlds/[WorldName]`
- **Input Files**:
    - `canon/world_config.json` (Reads Title, existing fields)
    - `prompts/WORLD_BUILDER.md` (The Prompt Template)
- **Prompt Logic**:
    - Loads `WORLD_BUILDER.md` (Overrides: `worlds/[World]/prompts/` > `prompts/`)
    - Injects: `{{TITLE}}`, `{{SETTING}}`, `{{THEME}}`, `{{GLITCH}}`, `{{CHARACTERS}}`
- **AI Task**: `generate_world`
- **Output**:
    - Updates `canon/world_config.json` with new/refined fields.

## 2. Planning: Brainstorming
**Goal**: Generate story concepts from source material.

- **GUI Action**: "Generate from Source" button.
- **API Endpoint**: `/api/generate/brainstorm`
- **Script**: `scripts/generate_brainstorm_iterative.py`
- **Input Files**:
    - `source/*` (Text/MD files for inspiration)
    - `prompts/BRAINSTORM_DISCOVERY.md` (Phase 1)
    - `prompts/BRAINSTORM_GENERATOR.md` (Phase 2)
- **Prompt Logic**:
    - **Phase 1 (Discovery)**: Scans source files. Uses `BRAINSTORM_DISCOVERY.md` to find interesting themes.
    - **Phase 2 (Generation)**: Uses `BRAINSTORM_GENERATOR.md` + Discovery Output to generate structured concepts.
- **Output**:
    - Creates `planning/BRAINSTORM_RAW.json` (List of concepts).

## 3. Planning: Chapter Map
**Goal**: Turn concepts into a high-level chapter outline.

- **GUI Action**: "Generate Map" button.
- **API Endpoint**: `/api/generate/map`
- **Script**: `scripts/generate_chapter_map.py`
- **Input Files**:
    - `planning/BRAINSTORM_RAW.json` (Approved concepts)
    - `canon/world_config.json`
    - `prompts/CHAPTER_MAP_GENERATOR.md`
- **Output**:
    - Creates `planning/CHAPTER_MAP.md`.

## 4. Planning: Chapter Cards
**Goal**: detailed beat sheets for each chapter.

- **GUI Action**: "Generate Cards" button.
- **API Endpoint**: `/api/generate/cards`
- **Script**: `scripts/generate_chapter_cards.py`
- **Input Files**:
    - `canon/TIMELINE.md` (or `CHAPTER_MAP.md` content if refined)
    - `canon/world_config.json`
    - `planning/BRAINSTORM.json` (Optional context)
    - `prompts/GENERATE_CARD.md`
- **Output**:
    - Creates `planning/chapter-cards/CH[xxx].md` for each chapter.

## 5. Drafting (Writing)
**Goal**: Turn cards into prose.

- **GUI Action**: "Generate Chapters" button on Workflow Panel.
- **API Endpoint**: `/api/generate/chapters`
- **Script**: `scripts/generate_chapters.py`
- **Input Files**:
    - `planning/chapter-cards/CH[xxx].md` (The primary source)
    - `canon/world_config.json`
    - `prompts/WRITER_INSTRUCTIONS.md` (Instructions on style/voice)
- **Output**:
    - Creates `chapters/CH[xxx]-[Title].md`.

## 6. Refinement Station
**Goal**: Polish and edit chapters using specific lenses.

- **GUI Action**: "Refine" button in Reader Mode.
- **API Endpoint**: `/api/refine`
- **Script**: `scripts/refine_chapters.py`
- **Pass Types & Prompts**:
    - **Writer Pass**: `prompts/WRITER_INSTRUCTIONS.md`
    - **Continuity**: `prompts/CC_INSTRUCTIONS.md`
    - **Style**: `prompts/SE_INSTRUCTIONS.md`
    - **QA**: `prompts/QA_INSTRUCTIONS.md`
    - **Product**: `prompts/PO_INSTRUCTIONS.md`
    - **Custom**: `prompts/IMPROVEMENT_IDEAS.md`
- **Input Files**:
    - `chapters/CH[xxx].md` (Current content)
    - `chapters/meta/CH[xxx].feedback.md` (User feedback, if any)
- **Prompt Logic**:
    - Uses `prompts/REFINE_CHAPTER.md` as the base wrapper.
    - Injects the specific Instruction content + Chapter Content.
- **Output**:
    - Saves refined version to `chapters/refined/CH[xxx].md`.

## 7. Steering & Customization
**Global vs. Local Prompts**:
- **Global**: Located in `/prompts/` (Project Root). Used as fallback.
- **Local (World)**: Located in `worlds/[WorldName]/prompts/`. **Always prioritized**.
- **Edit Logic**: The GUI's "Steering" tab allows you to edit the *World Specific* prompt, effectively overriding the AI's behavior for that project only.
