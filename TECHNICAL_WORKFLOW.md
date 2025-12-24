# Technical Workflow Guide V2 (Recursive Story Engine)
This document details the file operations, prompt templates, and scripts used by the **Recursive Story Engine** architecture ("The Alchemy of Character").

## 1. Inspiration Phase (Analysis)
**Goal**: Scan raw source material to extract narrative fuel (Themes, Atmosphere, Potential Ghosts) rather than generic beats.

- **GUI Action**: "Generate from Source" button.
- **API Endpoint**: `/api/generate/brainstorm` (Mapped to analysis script).
- **Script**: `scripts/analyze_source.py`
- **Context**: `cwd = worlds/[WorldName]`
- **Input Files**:
    - `source/*` (Raw text/MD files)
    - `prompts/AGENT_ANALYZER.md` (Analyzer Prompt)
- **Output**:
    - Creates `planning/INSPIRATION.md` (Themes, Atmosphere, Ghosts, Lies).

## 2. Foundation Phase (The 4-Agent Protocol)
**Goal**: Build a deep "Character-First" world bible (`STORY_CANON`) using a chain of specialized agents.

- **GUI Action**: "Auto-Generate (AI)" button on World Config page.
- **API Endpoint**: `/api/generate/world`
- **Script**: `scripts/build_foundations.py`
- **Flow**:
    1.  **Genesis Agent** (`prompts/AGENT_GENESIS.md`):
        -   Input: `planning/INSPIRATION.md`
        -   Output: `canon/01_CONCEPT/*` (Logline, Identity, Arc)
    2.  **Psyche Agent** (`prompts/AGENT_PSYCHE.md`):
        -   Input: `canon/01_CONCEPT/*`
        -   Output: `canon/02_CHARACTER_PROFILE/*` (Ghost, Goals/Motivations, Fatal Flaw, Worldview)
    3.  **Embodiment Agent** (`prompts/AGENT_EMBODIMENT.md`):
        -   Input: `canon/01_CONCEPT/*` + `canon/02_CHARACTER_PROFILE/*`
        -   Output: `canon/02_CHARACTER_PROFILE/*` (Physical, Voice Sample, Quirks)
    4.  **Crucible Agent** (`prompts/AGENT_CRUCIBLE.md`):
        -   Input: All previous outputs.
        -   Output: `canon/03_PLOT_DYNAMICS/*` (Conflict, Stakes, Cast, Midpoint)

## 3. Drafting Phase (Recursive Writing)
**Goal**: Write chapters using the "Scene/Sequel" rhythm and maintain perfect continuity via `[STORY_STATE]`.

- **GUI Action**: "Generate Chapters" button.
- **API Endpoint**: `/api/generate/chapters`
- **Script**: `scripts/generate_chapters.py`
- **Input Context**:
    -   **Previous Chapter**: Reads the last `[STORY_STATE]` block from the previous file (if exists).
    -   **Chapter Card**: `planning/chapter-cards/CH[xxx].md` (The Beat).
    -   **Prompt**: `prompts/WRITER_SCENE_SEQUEL.md`.
- **Logic**:
    -   Injects `[STORY_STATE]` into the prompt context.
    -   Writer Agent determines if the beat needs a **SCENE** (Goal/Conflict/Disaster) or **SEQUEL** (Reaction/Dilemma/Decision).
    -   **Strict Output Rule**: Must append an updated `[STORY_STATE]` block at the end of the text.
- **Output**:
    -   Creates `chapters/CH[xxx].md`.

## 4. Refinement Station
*(Unchanged in V2, but uses new prompt context if updated)*
**Goal**: Polish and edit chapters.

- **GUI Action**: "Refine" button in Reader Mode.
- **Script**: `scripts/refine_chapters.py`
- **Prompts**: `prompts/REFINE_CHAPTER.md` (+ instruction overlays).

## Directory Structure (V2)
```text
worlds/[WorldName]/
├── canon/
│   ├── 01_CONCEPT/ (Logline, Identity, Arc)
│   ├── 02_CHARACTER_PROFILE/ (Ghost, Goals, Flaw, Voice)
│   └── 03_PLOT_DYNAMICS/ (Conflicts, Stakes, Cast)
├── planning/
│   ├── INSPIRATION.md (Source analysis)
│   └── chapter-cards/ (Beat sheets)
├── chapters/
│   └── CH001.md (Contains [STORY_STATE] at EOF)
└── source/ (Raw inputs)
```
