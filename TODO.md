# Project Status & Migration Handoff (V2)

## 📍 Where We Are
We have successfully completed the massive "V2 Refactor" to support the **Recursive Story Engine**.

### 1. New Features (Completed)
- [x] **Recursive Engine**: `scripts/generate_chapters.py` now maintains continuity via `[STORY_STATE]`.
- [x] **Didactic Workflow (Phoenix Logic)**: New prompt (`AGENT_DIDACTIC_ARCHITECT`) and script (`generate_didactic_story.py`) to turn transcripts into business fables.
- [x] **Prompt Editor**: GUI now allows direct editing of prompts (pencils next to buttons).
- [x] **Frontend Integration**: "Generate Fable" button added to Brainstorm Review.

### 2. Documentation (Updated)
- `README.md`: Updated with V2 architecture.
- `AGENTS.md`: Updated with 4-Agent Protocol and Technical Specs.
- `QUICK_REFERENCE.md`: Updated for V2 workflow.
- `start_gui.sh`: REMOVED (Legacy workaround).

---

## 🚀 Immediate Next Steps (The Migration)
We are moving from the slow exFAT drive to your native home folder.

### 1. Clone to New Location
Run this on your machine:
```bash
# Create projects folder
mkdir -p ~/projects
cd ~/projects

# Clone fresh
git clone https://github.com/edunmore/nlpbook.git nlpbook-native
cd nlpbook-native
```

### 2. Setup Environment (One Time)
Run this inside `~/projects/nlpbook-native`:
```bash
# Backend Setup
python3 -m venv gui/backend/venv
source gui/backend/venv/bin/activate
pip install fastapi uvicorn

# Frontend Setup
cd gui/client
npm install
```

### 3. Start Working
Open VS Code in `~/projects/nlpbook-native`.
Terminals:
- **Backend**: `source gui/backend/venv/bin/activate && python gui/backend/main.py`
- **Frontend**: `cd gui/client && npm run dev`

---

## 🔮 Future Roadmap (Post-Migration)
Once settled in the new drive, we can tackle:
1.  **Refine Didactic Output**: Test the "Phoenix Logic" on real transcripts and tune the prompt.
2.  **Series Bible UI**: Build a dedicated GUI page for viewing/editing the `canon/` files.
3.  **Chat Interface**: Allow chatting with the "Didactic Architect" to refine the story interactively.
