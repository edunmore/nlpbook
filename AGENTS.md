# Agent Protocols

## Secure State Protocol
At the beginning of each session or major task:

1.  **Commit Everything**: Ensure all pending changes are committed to the current branch.
2.  **Secure State Branch**: Create a new branch to work on.
    -   **Naming Convention**: `session/<YYYY-MM-DD>_<TOPIC>`
    -   Example: `session/2025-12-23_refine_workflow`
3.  **Documentation**: Update this file if new protocols are established.

## 🚨 Critical System Constraints
**Filesystem Limitations**: The project lives on a mounted drive (`/media/mac/projects/nlpbook`) that **does not support execution or symlinks** for certain binaries (causing `Exec format error`).
**Solution**: We run the app from a **Shadow Workspace** at `/home/mac/.gemini/shadow_workspace`.

## 🚀 Session Startup Guide
1. **Sync Code**: Ensure the shadow workspace has the latest code.
   ```bash
   # Update shadow code (excluding heavy dirs)
   cp -r /media/mac/projects/nlpbook/{gui,scripts,prompts,process,README.md} /home/mac/.gemini/shadow_workspace/
   # Ensure worlds are symlinked (only needs to happen once, but harmless to check)
   ln -s /media/mac/projects/nlpbook/worlds /home/mac/.gemini/shadow_workspace/worlds
   ```
2. **Start Backend**:
   ```bash
   cd /home/mac/.gemini/shadow_workspace
   source venv/bin/activate
   python gui/backend/main.py
   ```
3. **Start Frontend**:
   ```bash
   cd /home/mac/.gemini/shadow_workspace/gui/client
   npm run dev
   ```

## 🛠️ Development Workflow
**Editing Code**:
1. Edit files in the **Original Project Directory** (`/media/mac/projects/nlpbook/...`).
2. **Immediately copy** the modified file to the shadow workspace to apply changes.
   `cp /path/to/original /home/mac/.gemini/shadow_workspace/path/to/shadow`
3. Verify in browser.

## 🧩 Template System & Decentralized Prompts
**New World Creation**:
- All new worlds are clones of `worlds/NEWORLDTEMPLATE`.
- **Canon**: `world_config.json`, `SERIES_BIBLE.md` etc are copied from the template.
- **Prompts**: `prompts/` and `process/` are copied to `worlds/[WorldName]/prompts/`.
- **Customization**: You can edit `worlds/[WorldName]/prompts/WRITER_INSTRUCTIONS.md` to change the AI's behavior *only for that world*.

## 🤖 Gemini Context Scoping
The `gemini` CLI is always executed with `cwd = worlds/[CurrentWorld]`.
- **Visibility**: The agent sees `canon/`, `chapters/`, and `Gemini.md` in the root.
- **Prompt Loading**: Scripts prioritize `worlds/[World]/prompts/[File]` over global defaults.
- **Gemini.md**: A file in the world root that gives the agent context about its role and file structure.

## 🧠 Solved Issues (Memory)
- **Storyline UI**: The "Storyline / Timeline" textarea was missing. Fixed in `WorldHelper.jsx` by adding a dedicated textarea bound to `TIMELINE.md` steering content.
- **Frontend/Backend Paths**: Frontend runs on :5173, Backend on :8000. Backend serves files from `worlds/`.
