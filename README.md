# BookAgent — AI-Assisted Novel Writing System

A comprehensive GUI-driven system for writing novels with AI assistance. It features a complete workflow from World Creation to Planning, Drafting, and Multi-Pass Refinement.

## 🚀 Key Features

### 1. World Builder
- **Custom Worlds**: Create unlimited isolated project environments (worlds).
- **AI Auto-Correction**: Use the "Auto-Generate (AI)" button to fill in world details (Theme, Setting, Glitch) based on natural language instructions.
- **Canon Management**: Automatically inherits style guides and rules while maintaining world-specific bibles.

### 2. Planning Workflow
- **Brainstorming**: Ingests source material (e.g., local text files) to generate unique story concepts.
- **Chapter Map**: Generates high-level outlines based on approved concepts.
- **Chapter Cards**: Creates detailed beat sheets for each chapter.
- **Visual Review**: Drag-and-drop or rating-based review system for all planning artifacts.

### 3. Drafting & Refinement Station
- **Chapter Generation**: Turns beat sheets into full prose.
- **Multi-Pass Refinement**: The "Refinement Station" allows you to apply specific editing passes to your content:
    - **Writer Pass**: Focuses on narrative voice and "show, don't tell".
    - **Continuity Check (CC)**: Verifies consistency with the Series Bible.
    - **Style Edit (SE)**: Fixes formatting and adherence to style guides.
    - **Quality Assurance (QA)**: Final polish.
    - **Product Review (PO)**: High-level thematic check.

### 4. Auto-Updating GUI
- **Real-Time Feedback**: The GUI polls the backend for progress and automatically refreshes content when AI tasks complete.
- **Seamless Editing**: Switch between "Reader Mode" and "Builder Mode" instantly.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js & npm
- Gemini CLI (or compatible agent capable of running prompts)

### 1. Backend Setup
```bash
python3 -m venv gui/backend/venv
source gui/backend/venv/bin/activate
pip install fastapi uvicorn
```

### 2. Frontend Setup
```bash
cd gui/client
npm install
```

### 3. Running the Application
Open two terminal tabs:

**Tab 1 (Backend):**
```bash
source gui/backend/venv/bin/activate
python gui/backend/main.py
```

**Tab 2 (Frontend):**
```bash
cd gui/client
npm run dev
```

Visit `http://localhost:5173` to start writing.

---

## 📖 Workflow Guide

### 1. Create a World
1. Select **"+ New World"** from the top-left dropdown.
2. Enter a name (e.g., "Neon-City").
3. Use the **World Config** tab to set your setting and theme. Try typing "AI: make it a solarpunk mystery" in the Theme field and clicking **Auto-Generate**.

### 2. Plan Your Book
1. Go to **Planning Workflow**.
2. **Brainstorm**: Click "Generate from Source" (requires source text in your world's source path) or add ideas manually.
3. **Approve**: Rate ideas 3+ stars to approve them.
4. **Map**: Click "Generate Map" to create an outline.
5. **Cards**: Generate detailed chapter cards.

### 3. Write & Refine
1. Generate chapters from your cards.
2. Click on a chapter in the sidebar to enter **Reader Mode**.
3. Use the **Refinement Station** on the right to improve the text. Select a pass (e.g., "Writer Pass") and click **Refine**.
4. The view will auto-update with the refined version upon completion.

---

## 📂 Directory Structure

- `worlds/` — Contains all user-created worlds.
    - `NEWORLDTEMPLATE/` — The master template for new worlds.
    - `[WorldName]/canon/` — Bibles, rules, and configs.
    - `[WorldName]/prompts/` — World-specific prompt overrides.
    - `[WorldName]/chapters/` — Markdown content files.
    - `[WorldName]/planning/` — Brainstorms and maps.
- `prompts/` — Global default prompts (fallback).
- `scripts/` — Python automation scripts called by the backend.
- `gui/` — React frontend and FastAPI backend.

---

## ⚠️ Notes
- **Backups**: The system modifies files in place or creates copies in `refined/`. Always use git for version control.
- **Legacy**: The `task_runner.py` CLI workflow is deprecated in favor of the GUI.
