# Quick Reference Card - Automation System

## Essential Commands

### Process One Stage

```bash
# Writer
python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"

# Character Curator
python scripts/task_runner.py -s "CC Doing" -i prompts/CC_INSTRUCTIONS.md -f "CC Done"

# Style Editor
python scripts/task_runner.py -s "SE Doing" -i prompts/SE_INSTRUCTIONS.md -f "SE Done"

# QA
python scripts/task_runner.py -s "QA Doing" -i prompts/QA_INSTRUCTIONS.md -f "Finished"

# PO Review
python scripts/task_runner.py -s "PO Review" -i prompts/PO_INSTRUCTIONS.md -f "Finished"
```

### Process Complete Pipeline

```bash
# Interactive mode
python scripts/batch_process.py

# Automated mode
python scripts/batch_process.py --no-interactive

# Process 3 tasks per stage
python scripts/batch_process.py --limit 3
```

### Planning & Inspiration

```bash
# Iterative Brainstorm (loops through NLP/ source)
python scripts/generate_brainstorm_iterative.py --world [name]

# Generate Chapter Map from approved concepts
python scripts/generate_chapter_map.py --world [name] --count 10

# Evaluate a book plan
python scripts/evaluate_plan.py --world [name]
```

## Common Options

| Flag | Description | Example |
|------|-------------|---------|
| `-s` | Source status | `-s "Writer Doing"` |
| `-i` | Instruction template | `-i prompts/WRITER_INSTRUCTIONS.md` |
| `-f` | Finish status | `-f "Writer Done"` |
| `--limit` | Max tasks to process | `--limit 5` |
| `--no-interactive` | No prompts | `--no-interactive` |
| `--workspace` | Workspace path | `--workspace /path/to/nlpbook` |

## Status Flow

```
Backlog → Writer Doing → Writer Done → CC Doing → CC Done → 
SE Doing → SE Done → QA Doing → Finished
```

## Template Variables

- `{{TASK_ID}}` - Task identifier
- `{{TASK_TITLE}}` - Task title  
- `{{TASK_DESCRIPTION}}` - Full description
- `{{TASK_NOTES}}` - Additional notes
- `{{CHAPTER_NUM}}` - Chapter number (extracted from title)

## File Locations

| Type | Location |
|------|----------|
| Main Script | `scripts/task_runner.py` |
| Batch Script | `scripts/batch_process.py` |
| Templates | `prompts/*.md` |
| Generated Instructions | `GEMINI.md` |
| Canon Files | `canon/` |
| Process Docs | `process/` |

## Troubleshooting

**No tasks found?**
- Check status spelling (case-sensitive)
- Verify tasks exist in backlog.md with that status

**Gemini CLI not found?**
- Install: https://github.com/google-gemini/gemini-cli
- Check PATH: `gemini --version`

**Template errors?**
- Check template path is relative to workspace
- Verify file exists in `prompts/`

## Quick Start

1. Move tasks to "Writer Doing" in backlog.md
2. Run: `python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"`
3. Continue through pipeline stages

## Getting Help

```bash
# Show help
python scripts/task_runner.py --help
python scripts/batch_process.py --help
```

## Documentation

- `AUTOMATION_SETUP.md` - Complete setup guide
- `MIGRATION_SUMMARY.md` - What changed and why
- `README.md` - Project overview
- `process/RUNBOOK.md` - Workflow guide
