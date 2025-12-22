# Example: Running Your First Automated Task

This example walks through processing a single Writer task using the new automation system.

## Scenario

You have a chapter task in backlog.md:
- **Task ID**: `task-001`
- **Title**: `CH001-The-Glitch-in-the-System`
- **Status**: `Writer Doing`
- **Description**: Write opening chapter introducing Elara...

## Step 1: Verify Prerequisites

```bash
# Check Gemini CLI is installed
$ gemini --version
gemini-cli version 1.0.0

# Check Python
$ python --version
Python 3.11.0

# Navigate to workspace
$ cd f:\nlpbook
```

## Step 2: Verify Task in Backlog

Your task should exist in backlog.md (managed via MCP) with:
- Status: `Writer Doing`
- All required fields filled

## Step 3: Run the Automation

```bash
$ python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"
```

### What Happens:

```
================================================================================
📚 Novel-as-Software Task Runner
================================================================================
Source Status: Writer Doing
Instruction Template: prompts/WRITER_INSTRUCTIONS.md
Finish Status: Writer Done
Workspace: f:\nlpbook
================================================================================

📋 Querying tasks with status: Writer Doing

📊 Found 1 task(s) to process

────────────────────────────────────────────────────────────────────────────────
Task 1/1: CH001-The-Glitch-in-the-System
────────────────────────────────────────────────────────────────────────────────
Process this task? [Y/n/q]: Y

📝 Created instruction file: f:\nlpbook\GEMINI.md

🚀 Running Gemini CLI...
   Command: gemini -p Please complete the task described in GEMINI.md following all instructions carefully. -y

✅ Gemini CLI completed successfully
✅ Task 'CH001-The-Glitch-in-the-System' completed and moved to 'Writer Done'

================================================================================
✅ Task runner completed
================================================================================
```

## Step 4: What Was Created

### GEMINI.md (auto-generated)

```markdown
# Writer Task Instructions

**Task**: CH001-The-Glitch-in-the-System  
**Chapter**: CH001  
**Task ID**: task-001

---

## Your Role: Writer (DraftService)

You are drafting chapter prose from the Chapter Card and canon materials.

## Current Task

Write opening chapter introducing Elara, her world as a UX designer,
and the initial "glitch" - both in her software project and in her
personal patterns of responding to stress...

## Required Inputs (Read These Files)

- canon/SERIES_BIBLE.md
- canon/CONTINUITY_LEDGER.md
- canon/TIMELINE.md
- canon/OPEN_LOOPS.md
- canon/STYLE_RULES.md
- canon/BANNED_TERMS.txt
- planning/chapter-cards/CH001.md (if exists)

[... rest of instructions ...]
```

## Step 5: Verify Results

### In Backlog.md (via MCP)

Task status updated:
- **Before**: `Writer Doing`
- **After**: `Writer Done`
- **Notes**: Automated processing completed at 2025-12-16 14:32:00

### Chapter Content

The completed chapter should now be in the task notes in backlog.md, including:
- Full chapter prose
- SERIES MEMORY UPDATE section
- Purpose/Theme statement

## Step 6: Continue Pipeline

Move the task to the next stage:

```bash
# In backlog.md, change status from "Writer Done" → "CC Doing"

# Then run Character Curator
$ python scripts/task_runner.py -s "CC Doing" -i prompts/CC_INSTRUCTIONS.md -f "CC Done"
```

## Alternative: Run Complete Pipeline

Instead of running each stage manually, use the batch processor:

```bash
$ python scripts/batch_process.py --limit 1
```

This will:
1. Process Writer tasks (Writer Doing → Writer Done)
2. Ask if you want to continue
3. Process CC tasks (CC Doing → CC Done)  
4. Ask if you want to continue
5. Process SE tasks (SE Doing → SE Done)
6. Ask if you want to continue
7. Process QA tasks (QA Doing → Finished)

## Fully Automated Example

For completely hands-off processing:

```bash
# Process first 3 tasks through entire pipeline without any prompts
$ python scripts/batch_process.py --limit 3 --no-interactive
```

## Troubleshooting This Example

### "No tasks found with status 'Writer Doing'"

**Solution**: 
1. Check backlog.md has tasks with exact status "Writer Doing" (case-sensitive)
2. Verify backlog.md MCP is running and accessible
3. Try: `python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done" --workspace f:\nlpbook`

### "Template file not found"

**Solution**:
1. Verify you're in the workspace root: `cd f:\nlpbook`
2. Check template exists: `dir prompts\WRITER_INSTRUCTIONS.md`
3. Use correct relative path from workspace root

### "Gemini CLI not found"

**Solution**:
1. Install Gemini CLI from https://github.com/google-gemini/gemini-cli
2. Add to PATH
3. Verify: `gemini --version`

## Expected Timeline

For a typical chapter:
- **Writer stage**: 5-15 minutes (depending on chapter complexity)
- **CC stage**: 3-5 minutes (continuity check + canon updates)
- **SE stage**: 3-5 minutes (style polish)
- **QA stage**: 2-3 minutes (DoD verification)
- **Total**: ~15-30 minutes per chapter

## Success Indicators

✅ Script completes without errors  
✅ Task status updated in backlog.md  
✅ Chapter content appears in task notes  
✅ SERIES MEMORY UPDATE section present  
✅ Canon files updated (for CC stage)  
✅ No banned terms used (checked by SE/QA)  

## Next Steps

1. Review the completed chapter in backlog.md
2. If satisfied, move to next stage: "Writer Done" → "CC Doing"
3. Run CC automation: `python scripts/task_runner.py -s "CC Doing" ...`
4. Continue through SE → QA → Finished
5. Or use batch processor for the whole pipeline

## Tips

💡 **Start small**: Process 1 task first with `--limit 1`  
💡 **Interactive mode**: Leave interactive on until comfortable  
💡 **Check GEMINI.md**: Review generated instructions if results are unexpected  
💡 **Status transitions**: You may need to manually move tasks between stages in backlog.md  
💡 **Batch processing**: Use `batch_process.py` once individual stages are working well  

---

**Congratulations!** You've completed your first automated task. The system is now handling all the manual coordination work, letting you focus on the creative decisions.
