# Technical Workflow Guide
This document details the exact file operations, prompt templates, and scripts used by each stage of the BookAgent workflow. It is the technical source of truth.

## 1. World Generation
**Goal**: Initialize a new world with context (Setting, Theme, Characters).

- **GUI Action**: "Auto-Generate (AI)" button on World Config page.
- **API Endpoint**: `/api/generate/world`
- **Script**: `scripts/generate_world.py`
- **Context**: `cwd = worlds/[WorldName]`
- **Input Files**:
    - `canon/world_config.json` (Reads Title, existing fields) // I assume this is saved when the World Config page is saved
    - `prompts/WORLD_BUILDER.md` (The Prompt Template)
- **Prompt Logic**:
    - Loads `WORLD_BUILDER.md` (Overrides: `worlds/[World]/prompts/` > `prompts/`) // this is executed when the World Config Auto-Generate (AI) button is clicked
    - Injects: `{{TITLE}}`, `{{SETTING}}`, `{{THEME}}`, `{{GLITCH}}`, `{{CHARACTERS}}`
- **AI Task**: `generate_world`
- **Output**:
    - Updates `canon/world_config.json` with new/refined fields.

// WORD BUILDER is quite generic as instructions - I think we need better foundation material for this - see the /lernwriting folder for inspiration 
// my general question is, is it the right point??? Wouldnt we need refinements ones we have more material? Or better - shouldnt be the brainstorm with the source
// happen before all that? Like what are we doing here? We do not know anything whats the book is all about, right? No inspiration nothing. I assume in the past it
// was working, as we had old information in the canon from the default world, but as we cleaned all that, we need to rethink this. 
// on the other hand, I should do that on my own - create the world with some data, than brainstorm and come back to refine the character???

## 2. Planning: Brainstorming   
**Goal**: Generate story concepts from source material.

// I thought we iterate through the source file and let the AI generate for each file and not give it all files to avoid context overflow. For that the discovery should be more clear - we are looking for topics which would support our story from the source. For inspiration. We might give it the brainstorm list we have so far, so it might add to it. Or is it doing this like this already??? 
// the goal would not to get characters etc. but to get inspiration from the source - like from a NLP source which talks about peripheral vision to give you more perpective - we do not need a story from that already. We need the best inspiration from the source, maybe how this is described in the source. The stories itself we would create later on. Or I am confused by the whole concept now. Comes back to - check out lernwriting folder for how we should do it.

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
