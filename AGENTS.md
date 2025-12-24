# Agent Protocols (V2)

## 1. 4-Agent Foundation Protocol
The V2 engine uses four specialized agents to build the narrative foundation.
These prompts are located in `prompts/` and are fully editable via the GUI ("Configure Agents").

### 🧬 Genesis (The Architect)
- **Role**: Distills source material into a core narrative identity.
- **Output**: `01_STORY_GENESIS/01_LOGLINE_AND_ARC.md`
- **Key Responsibility**: Establishing the "Narrative spine" and the protagonist's core arc.

### 🧠 Psyche (The Psychologist)
- **Role**: Defines the internal landscape of the character.
- **Output**: `02_CHARACTER_PROFILE/01_INTERNAL_PSYCHE.md`
- **Key Concepts**:
    - **Ghost**: A past trauma haunting the character.
    - **Lie**: A misconception about the world born from the Ghost.
    - **Need**: The truth the character must learn to overcome the Lie.

### 👤 Embodiment (The Actor)
- **Role**: Translates internal traits into external reality.
- **Output**: `02_CHARACTER_PROFILE/02_EXTERNAL_EMBODIMENT.md`
- **Responsibility**: Defining voice, appearance, sensory details, and quirks.

### 🔥 Crucible (The Director)
- **Role**: Sets the stage and the stakes.
- **Output**: `01_STORY_GENESIS/02_CRUCIBLE_AND_CAST.md`
- **Key Responsibility**: Defining the Inciting Incident, Antagonist, and the "Midpoint" turning point.

---

## 2. Recursive Drafting Protocol
### ✍️ Writer (The Drafter)
- **Prompt**: `WRITER_SCENE_SEQUEL.md`
- **Methodology**: Writes in "Scene" (Action) and "Sequel" (Reflection) pairs.
- **State Management**: Reads and updates a `[STORY_STATE]` block at the end of every chapter to maintain continuity across context windows.

---

---

## 3. Technical Reference
**System Architecture**:
- **Backend**: Python (FastAPI) on port 8000.
- **Frontend**: Vite (React) on port 5173.
- **Filesystem**: Project lives on exFAT mount. No symlinks or execution bits allowed.
- **Execution**: Frontend must be run via `node` directly (`node node_modules/vite/bin/vite.js`).

## 🧩 Template System
**New World Creation**:
- All new worlds are clones of `worlds/NEWORLDTEMPLATE`.
- **Canon**: `world_config.json`, `SERIES_BIBLE.md`.
- **Prompts**: Editable copies of Genesis, Psyche, etc., are placed in `worlds/[WorldName]/prompts/`.

## 🤖 Gemini Context
The `gemini` CLI is executed with `cwd = worlds/[CurrentWorld]`.
- **Visibility**: The agent sees `canon/`, `chapters/`, and `Gemini.md`.
- **Priority**: World-specific prompts override global defaults.
