
# Runbook (How to run the automated pipeline)

## Automated Workflow

The pipeline is now automated using Python scripts that interact with Gemini CLI in headless mode.

### Setup
1. Ensure Gemini CLI is installed: [gemini-cli](https://github.com/google-gemini/gemini-cli)
2. Verify backlog.md MCP is configured for task management
3. Review and update canon files as needed

### Step-by-Step Process

1) **PO selects tasks**: Move N chapter tasks to `Writer Doing` status in backlog
2) **Run Writer automation**:
   ```bash
   python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"
   ```
   - Drafts chapter prose
   - Appends SERIES MEMORY UPDATE
   - Moves to `Writer Done`

3) **Run Continuity Curator automation**:
   ```bash
   python scripts/task_runner.py -s "CC Doing" -i prompts/CC_INSTRUCTIONS.md -f "CC Done"
   ```
   - Checks against canon
   - Updates canon files
   - Moves to `CC Done` or sends back for rework

4) **Run Style Editor automation**:
   ```bash
   python scripts/task_runner.py -s "SE Doing" -i prompts/SE_INSTRUCTIONS.md -f "SE Done"
   ```
   - Removes explaining/jargon
   - Enforces voice
   - Moves to `SE Done` or sends back for rework

5) **Run QA automation**:
   ```bash
   python scripts/task_runner.py -s "QA Doing" -i prompts/QA_INSTRUCTIONS.md -f "Finished"
   ```
   - Verifies DoD
   - Moves to `Finished` or sends back for rework

6) **PO Review** (if needed):
   ```bash
   python scripts/task_runner.py -s "PO Review" -i prompts/PO_INSTRUCTIONS.md -f "Finished"
   ```
   - PO accepts → `Finished`
   - Or sends to `Writer Doing` with REWORK notes

7) **After each sprint**: PO Review + Retro tasks produce process updates

### Manual Task Status Management

Between automated runs, you can manually move tasks through statuses in backlog.md:
- Move completed tasks from `Writer Done` → `CC Doing`
- Move completed tasks from `CC Done` → `SE Doing`
- Move completed tasks from `SE Done` → `QA Doing`
- Or use automation flags to handle the full pipeline

### Options for Automation

```bash
# Process only first 3 tasks
python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done" --limit 3

# Run without interactive prompts
python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done" --no-interactive

# Specify workspace
python scripts/task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done" --workspace /path/to/nlpbook
```
