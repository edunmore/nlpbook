# Quick Reference Card - BookAgent GUI (V2)

## 🚀 Essential Activity

### Startup
1. **Backend**: `source gui/backend/venv/bin/activate && python gui/backend/main.py`
2. **Frontend**: `cd gui/client && node node_modules/vite/bin/vite.js`
3. **Visit**: `http://localhost:5173`

### World & Agent Config
- **New World**: `+ New World` from dropdown.
- **Configure Agents**: Next to "Auto-Generate", click **Genesis**, **Psyche**, etc. to edit their prompts.
- **Prompt Editor**: Click the **Edit (pencil)** icon to customize AI instructions for that specific world.

### Planning Pipeline (Alchemy)
1. **Source**: Ingest text files via "Generate from Source" (Edit `AGENT_ANALYZER` first!).
2. **Brainstorm**: Approve concepts (3+ stars).
3.  **Map & Cards**: Generate outlines and beat sheets.

---

## 📂 File Structure (V2)

| Folder                    | Contents                                          |
| ------------------------- | ------------------------------------------------- |
| `worlds/[name]/prompts/`  | **User-Editable Prompts** (Genesis, Writer, etc.) |
| `worlds/[name]/canon/`    | `01_STORY_GENESIS`, `02_CHARACTER_PROFILE`        |
| `worlds/[name]/chapters/` | Drafted & Refined Prose                           |
| `worlds/[name]/planning/` | Brainstorms, Maps, Cards                          |

---

## 🛠️ Agents (V2)
- **Genesis**: Logline & Arc.
- **Psyche**: Ghost, Lie, Need.
- **Embodiment**: Voice & Appearance.
- **Crucible**: Plot Stakes.
- **Writer**: Recursive Scene/Sequel drafting.

## 📄 Documentation
- `README.md` - System Overview.
- `GUI_WORKFLOW.md` - Visual User Guide.
- `AGENTS.md` - Technical Protocol Reference.
