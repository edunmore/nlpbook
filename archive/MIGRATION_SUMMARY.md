# Migration Summary: Manual to Automated Workflow

## What Changed

### Old System (Manual)
- Manually instructed agents via chat/prompts
- Agent had to read `backlog://workflow/overview` from MCP
- Agent searched for tasks with specific status
- Agent processed tasks one by one
- Agent updated task status manually
- Heavy reliance on agent understanding the workflow

### New System (Automated)
- Python script (`task_runner.py`) handles everything
- Script queries backlog via MCP automatically
- Script loads instruction templates with task variables
- Script populates `GEMINI.md` with complete instructions
- Script calls Gemini CLI in headless mode: `gemini -p "prompt" -y`
- Script updates task status on completion
- Consistent, repeatable process

## Files Created

### Core Automation
1. **scripts/task_runner.py** - Main automation script
   - Queries tasks by status
   - Loads and populates templates
   - Executes Gemini CLI
   - Updates task status

2. **scripts/batch_process.py** - Pipeline orchestration
   - Runs complete Writer → CC → SE → QA → PO pipeline
   - Batch processing support
   - Error handling and reporting

### Instruction Templates
Located in `prompts/`:
1. **WRITER_INSTRUCTIONS.md** - Chapter writing template
2. **CC_INSTRUCTIONS.md** - Character Curator/Continuity template
3. **SE_INSTRUCTIONS.md** - Style Editor template
4. **QA_INSTRUCTIONS.md** - Quality Assurance template
5. **PO_INSTRUCTIONS.md** - Product Owner review template

Each template uses variables like `{{TASK_ID}}`, `{{TASK_TITLE}}`, `{{CHAPTER_NUM}}`, etc.

### Documentation
1. **AUTOMATION_SETUP.md** - Complete setup and usage guide
2. **MIGRATION_SUMMARY.md** - This file

## Files Modified

### Core Documentation
1. **README.md**
   - Updated workflow description
   - Added automation commands
   - Added requirements section
   - Updated repo folder descriptions

2. **GEMINI.md**
   - Removed MCP workflow instructions
   - Now a template file populated by automation
   - Contains placeholder variables

### Process Files
1. **process/RUNBOOK.md**
   - Replaced manual steps with automation commands
   - Added command-line examples
   - Documented options and flags

2. **process/WORKING_AGREEMENTS.md**
   - Updated to mention automation system

### Agent Files (Reference Documentation)
All files in `agents/` folder updated to mention automation:
1. **AGENTS-WRITER.md** - Added automation reference
2. **AGENTS-CHARACTER-CURATOR.md** - Added automation reference
3. **AGENTS-STYLE_EDITOR.md** - Added automation reference
4. **AGENTS-QA.md** - Added automation reference
5. **AGENTS-PO.md** - Added automation reference
6. **AGENTS-BACKLOG-STEWARD.md** - Updated for automation context

These are now reference documentation rather than operational instructions.

## Command Reference

### Single Stage Processing

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

### Complete Pipeline

```bash
# Interactive (asks before each stage)
python scripts/batch_process.py

# Automated (no prompts)
python scripts/batch_process.py --no-interactive

# Limit tasks per stage
python scripts/batch_process.py --limit 3

# Start from specific stage
python scripts/batch_process.py --start-from cc
```

## How It Works

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ User runs: python task_runner.py -s "Writer Doing" ...     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Query backlog.md MCP for tasks with status="Writer Doing"│
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Load template: prompts/WRITER_INSTRUCTIONS.md            │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Substitute variables:                                    │
│    {{TASK_ID}} → "task-123"                                 │
│    {{TASK_TITLE}} → "CH001-The-Glitch-in-the-System"       │
│    {{CHAPTER_NUM}} → "001"                                  │
│    etc.                                                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Write complete instructions to GEMINI.md                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Execute: gemini -p "Complete task in GEMINI.md" -y      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. If successful, update task status to "Writer Done"      │
└─────────────────────────────────────────────────────────────┘
```

### Template Variable Substitution

Before:
```markdown
# Task: {{TASK_TITLE}}
Chapter: CH{{CHAPTER_NUM}}
ID: {{TASK_ID}}

## Description
{{TASK_DESCRIPTION}}
```

After (populated):
```markdown
# Task: CH001-The-Glitch-in-the-System
Chapter: CH001
ID: task-123

## Description
Write the opening chapter introducing Elara and the initial glitch...
```

## Benefits of Automation

### ✅ Consistency
- Every task gets exactly the same instructions
- No variation based on how you phrase requests
- Template-based approach ensures completeness

### ✅ Efficiency
- No need to manually instruct agent each time
- Batch processing support
- Pipeline can run unattended

### ✅ Repeatability
- Same commands produce same results
- Easy to troubleshoot
- Clear audit trail

### ✅ Scalability
- Process multiple tasks with --limit flag
- Run entire pipeline with batch_process.py
- Easy to parallelize in the future

### ✅ Maintainability
- Templates in one place (`prompts/`)
- Easy to update instructions
- Version control friendly

## Migration Checklist

- [x] Created `task_runner.py` automation script
- [x] Created `batch_process.py` pipeline orchestrator
- [x] Created instruction templates for all roles
- [x] Updated `GEMINI.md` to be automation-friendly
- [x] Updated `README.md` with new workflow
- [x] Updated `process/RUNBOOK.md` with automation steps
- [x] Updated all agent files to reference automation
- [x] Created comprehensive setup documentation

## Next Steps

### To Start Using the System

1. **Install Prerequisites**
   ```bash
   # Install Gemini CLI
   # See: https://github.com/google-gemini/gemini-cli
   ```

2. **Verify Setup**
   ```bash
   # Check Gemini CLI
   gemini --version
   
   # Check Python
   python --version  # Should be 3.8+
   
   # Verify backlog.md MCP is configured
   ```

3. **Run Your First Task**
   ```bash
   # Move a task to "Writer Doing" in backlog.md
   
   # Run automation
   python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"
   ```

4. **Try Batch Processing**
   ```bash
   # Process entire pipeline for up to 3 tasks
   python scripts/batch_process.py --limit 3
   ```

### Customization

- Edit templates in `prompts/` to adjust instructions
- Modify `task_runner.py` for custom workflows
- Create new templates for additional roles
- Adjust status names in `process/BACKLOGMD_STATUS_POLICY.md`

## Support

For issues or questions:
1. Check `AUTOMATION_SETUP.md` for detailed documentation
2. Review `process/RUNBOOK.md` for workflow guidance
3. Verify `prompts/` templates have correct variables
4. Test with `--limit 1` flag to process one task at a time

## System Requirements

- **Python**: 3.8 or higher
- **Gemini CLI**: Latest version from https://github.com/google-gemini/gemini-cli
- **Backlog.md MCP**: Configured and running
- **Operating System**: Windows, macOS, or Linux

## Status Flow Reference

```
Backlog
  ↓
Writer Doing  →  Writer Done
                      ↓
                 CC Doing  →  CC Done
                                 ↓
                            SE Doing  →  SE Done
                                            ↓
                                       QA Doing  →  PO Review
                                                        ↓
                                                   Finished

Rework Flow (any stage):
Current Stage → Previous Stage's "Doing" status
(with REWORK notes appended)
```

## Key Differences Table

| Aspect | Old System | New System |
|--------|-----------|------------|
| Task Query | Manual MCP resource read | Automated via Python |
| Instructions | Typed manually each time | Template-based with variables |
| Execution | Agent interprets directly | Gemini CLI headless mode |
| Status Updates | Manual or agent-driven | Automated by script |
| Batch Processing | One at a time | Limit flag + batch_process.py |
| Consistency | Varies by prompt | Template ensures consistency |
| Troubleshooting | Check chat history | Check GEMINI.md + logs |
| Scalability | Limited | Highly scalable |

---

**You're all set!** The system is now automated and ready to use. Start with `python scripts/batch_process.py --limit 1` to test the complete pipeline.
