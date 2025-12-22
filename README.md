# The Coder and the Compass — Novel-as-Software Starter Kit

This repo is a starter layout to write a cohesive novel using a Scrum/Kanban-inspired agent workflow coordinated via backlog.md and automated with Python.

## Workflow Overview

### Automated Task Processing

The workflow is now automated using `scripts/task_runner.py` which:
1. Reads tasks from backlog.md (via MCP) with a specific status
2. Loads instruction templates for the current role
3. Populates GEMINI.md with task-specific instructions
4. Executes Gemini CLI in headless mode to process the task
5. Updates task status upon completion

### Status Flow

Backlog → Writer Doing → Writer Done → CC Doing → CC Done → SE Doing → SE Done → QA Doing → PO Review → Finished

**Rework rule**: The current role moves the task back to the previous role's **Doing** status and appends a note starting with `REWORK (<ROLE>):`.

### Running the Automation

```bash
# Process Writer tasks
python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"

# Process Character Curator tasks  
python scripts/task_runner.py -s "CC Doing" -i prompts/CC_INSTRUCTIONS.md -f "CC Done"

# Process Style Editor tasks
python scripts/task_runner.py -s "SE Doing" -i prompts/SE_INSTRUCTIONS.md -f "SE Done"

# Process QA tasks
python scripts/task_runner.py -s "QA Doing" -i prompts/QA_INSTRUCTIONS.md -f "Finished"

# Process PO Review tasks
python scripts/task_runner.py -s "PO Review" -i prompts/PO_INSTRUCTIONS.md -f "Finished"
```

### Options

- `--limit N`: Process only N tasks
- `--no-interactive`: Run without confirmation prompts
- `--workspace PATH`: Specify workspace directory

## Where the chapter text lives

Primary: store the full chapter markdown in the backlog task notes (see `process/NOTES_FORMAT.md`).
Optional: also export chapters into `chapters/` as files for versioning.

## Planning Workflow & Inspiration System

A GUI-driven workflow is available for generating and reviewing book plans:

1. **Inspiration System**: Loops through source files (e.g., `NLP/`) to extract story concepts.
2. **Iterative Planning**:
   - **Brainstorm Review**: Rate and approve concepts in the GUI.
   - **Chapter Map**: Generate and edit the book outline based on approved concepts.
   - **Chapter Cards**: Generate and review detailed planning cards one-by-one.
   - **Chapters**: Generate and review full chapters one-by-one.
3. **Canon Inheritance**: New worlds automatically inherit banned terms and style rules, with templates for series bibles and continuity ledgers.

To access the UI, run `npm run dev` in `gui/client` and visit the **Planning Workflow** tab.

## Repo folders

- `worlds/` — Multi-world directory structure. Each world has its own `canon/`, `planning/`, `chapters/`, and `history/`.
- `canon/` — Global canon templates (Style rules, Banned terms).
- `planning/` — Global planning templates.
- `prompts/` — Instruction templates for automated workflow and workflow generators.
- `scripts/` — python automation, brainstorm generators, map generators, and lint scripts.
- `gui/` — React frontend and FastAPI backend for the World Builder.
- `NLP/` — Source material for chapter ideas.

## Quick start

1) Review and edit `canon/SERIES_BIBLE.md`, `canon/STYLE_RULES.md`, and `canon/BANNED_TERMS.txt`.
2) Ensure backlog.md MCP is configured and tasks are created in backlog
3) Move 1–3 chapter tasks to `Writer Doing` status
4) Run the automation: `python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"`
5) Follow the handoffs until `Finished`
6) Optional: Run checks:
   - `python scripts/lint_banned_terms.py`
   - `python scripts/lint_structure.py`

## Requirements

- Python 3.8+
- Gemini CLI installed and in PATH ([gemini-cli](https://github.com/google-gemini/gemini-cli))
- Backlog.md MCP configured for task management
