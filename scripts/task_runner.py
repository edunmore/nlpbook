#!/usr/bin/env python3
"""
Task Runner for Novel-as-Software Project

This script automates the execution of tasks through Gemini CLI in headless mode.
It reads tasks from backlog.md with a specific status, processes them one by one
using instruction templates, and updates task status upon completion.

Usage:
    python task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"
    python task_runner.py -s "CC Doing" -i prompts/CC_INSTRUCTIONS.md -f "CC Done"
"""

import argparse
import subprocess
import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Optional


class BacklogTaskManager:
    """Manages reading and updating tasks in backlog.md via MCP tools."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.backlog_config = workspace_root / "backlog" / "config.yml"
        
    def get_tasks_by_status(self, status: str) -> List[Dict]:
        """
        Get all tasks with a specific status from backlog.
        Uses backlog.md MCP to query tasks.
        
        Returns list of task dictionaries with: id, title, status, description, notes
        """
        # This would normally call the MCP tool, but for now we'll use a placeholder
        # In real implementation, this would use the backlog MCP API
        print(f"📋 Querying tasks with status: {status}")
        
        # Placeholder - in production this would call:
        # backlog.search_tasks(status=status)
        # For now, return empty list as we need to integrate with MCP
        
        tasks = []
        # TODO: Integrate with backlog.md MCP to actually fetch tasks
        # For now, assume tasks are fetched via MCP
        
        return tasks
    
    def update_task_status(self, task_id: str, new_status: str, notes: Optional[str] = None) -> bool:
        """
        Update a task's status in backlog.md.
        
        Args:
            task_id: The task identifier
            new_status: The new status to set
            notes: Optional notes to append to the task
        
        Returns:
            True if update successful, False otherwise
        """
        print(f"✅ Updating task {task_id} to status: {new_status}")
        
        # TODO: Integrate with backlog.md MCP to update task
        # backlog.update_task(id=task_id, status=new_status, notes=notes)
        
        return True


class InstructionProcessor:
    """Processes instruction templates with variable substitution."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        
    def load_template(self, template_path: Path) -> str:
        """Load instruction template file."""
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def substitute_variables(self, template: str, task: Dict) -> str:
        """
        Replace variables in template with task-specific values.
        
        Supported variables:
            {{TASK_ID}} - Task identifier
            {{TASK_TITLE}} - Task title
            {{TASK_DESCRIPTION}} - Task description
            {{TASK_NOTES}} - Task notes/details
            {{CHAPTER_NUM}} - Extracted chapter number (if applicable)
        """
        result = template
        
        # Extract chapter number from title if present
        chapter_match = re.search(r'CH(\d+)', task.get('title', ''))
        chapter_num = chapter_match.group(1) if chapter_match else 'N/A'
        
        replacements = {
            '{{TASK_ID}}': task.get('id', ''),
            '{{TASK_TITLE}}': task.get('title', ''),
            '{{TASK_DESCRIPTION}}': task.get('description', ''),
            '{{TASK_NOTES}}': task.get('notes', ''),
            '{{CHAPTER_NUM}}': chapter_num,
        }
        
        for var, value in replacements.items():
            result = result.replace(var, str(value))
        
        return result
    
    def create_gemini_instruction(self, instruction_content: str, output_path: Path) -> None:
        """Write the processed instruction to GEMINI.md."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(instruction_content)
        
        print(f"📝 Created instruction file: {output_path}")


class GeminiCLIRunner:
    """Executes Gemini CLI in headless mode."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        
    def run_task(self, prompt: str, timeout: int = 300) -> tuple[bool, str]:
        """
        Execute Gemini CLI in headless mode.
        
        Args:
            prompt: The prompt to send to Gemini
            timeout: Timeout in seconds (default 5 minutes)
        
        Returns:
            Tuple of (success: bool, output: str)
        """
        cmd = [
            'gemini',
            '-p', prompt,
            '-y'  # Auto-accept prompts (headless mode)
        ]
        
        print(f"🚀 Running Gemini CLI...")
        print(f"   Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.workspace_root),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                print("✅ Gemini CLI completed successfully")
                return True, result.stdout
            else:
                print(f"❌ Gemini CLI failed with return code {result.returncode}")
                print(f"   Error: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Gemini CLI timed out after {timeout} seconds")
            return False, "Timeout expired"
        except FileNotFoundError:
            print("❌ Gemini CLI not found. Please ensure it's installed and in PATH.")
            return False, "Gemini CLI not found"
        except Exception as e:
            print(f"❌ Unexpected error running Gemini CLI: {e}")
            return False, str(e)


class TaskRunner:
    """Main orchestrator for the task automation system."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.task_manager = BacklogTaskManager(workspace_root)
        self.instruction_processor = InstructionProcessor(workspace_root)
        self.gemini_runner = GeminiCLIRunner(workspace_root)
        self.gemini_file = workspace_root / "GEMINI.md"
        
    def run(self, source_status: str, instruction_template: str, finish_status: str,
            limit: Optional[int] = None, interactive: bool = True) -> None:
        """
        Main execution loop.
        
        Args:
            source_status: Status to pull tasks from (e.g., "Writer Doing")
            instruction_template: Path to instruction template file
            finish_status: Status to set after successful completion
            limit: Optional limit on number of tasks to process
            interactive: If True, ask for confirmation before each task
        """
        print("\n" + "="*80)
        print("📚 Novel-as-Software Task Runner")
        print("="*80)
        print(f"Source Status: {source_status}")
        print(f"Instruction Template: {instruction_template}")
        print(f"Finish Status: {finish_status}")
        print(f"Workspace: {self.workspace_root}")
        print("="*80 + "\n")
        
        # Load instruction template
        template_path = self.workspace_root / instruction_template
        try:
            template = self.instruction_processor.load_template(template_path)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)
        
        # Get tasks with source status
        tasks = self.task_manager.get_tasks_by_status(source_status)
        
        if not tasks:
            print(f"ℹ️  No tasks found with status '{source_status}'")
            print("\n💡 Note: Backlog MCP integration is required.")
            print("   Tasks must be managed through backlog.md MCP system.")
            return
        
        if limit:
            tasks = tasks[:limit]
        
        print(f"📊 Found {len(tasks)} task(s) to process\n")
        
        # Process each task
        for idx, task in enumerate(tasks, 1):
            print(f"\n{'─'*80}")
            print(f"Task {idx}/{len(tasks)}: {task.get('title', 'Untitled')}")
            print(f"{'─'*80}")
            
            if interactive:
                response = input("Process this task? [Y/n/q]: ").strip().lower()
                if response == 'q':
                    print("🛑 Stopped by user")
                    break
                if response == 'n':
                    print("⏭️  Skipped")
                    continue
            
            # Substitute variables in template
            instruction_content = self.instruction_processor.substitute_variables(template, task)
            
            # Write to GEMINI.md
            self.instruction_processor.create_gemini_instruction(
                instruction_content, 
                self.gemini_file
            )
            
            # Create prompt for Gemini CLI
            prompt = f"Please complete the task described in GEMINI.md following all instructions carefully."
            
            # Run Gemini CLI
            success, output = self.gemini_runner.run_task(prompt)
            
            if success:
                # Update task status to finished
                self.task_manager.update_task_status(
                    task['id'],
                    finish_status,
                    notes=f"Automated processing completed at {self._get_timestamp()}"
                )
                print(f"✅ Task '{task.get('title')}' completed and moved to '{finish_status}'")
            else:
                print(f"❌ Task '{task.get('title')}' failed")
                print(f"   Output: {output}")
                
                if interactive:
                    retry = input("Retry this task? [y/N]: ").strip().lower()
                    if retry == 'y':
                        # Retry logic could go here
                        pass
        
        print("\n" + "="*80)
        print("✅ Task runner completed")
        print("="*80 + "\n")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Automate task processing through Gemini CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process Writer tasks
  python task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done"
  
  # Process Continuity Curator tasks
  python task_runner.py -s "CC Doing" -i prompts/CC_INSTRUCTIONS.md -f "CC Done"
  
  # Process with limit and non-interactive
  python task_runner.py -s "Writer Doing" -i prompts/WRITER_INSTRUCTIONS.md -f "Writer Done" --limit 3 --no-interactive
        """
    )
    
    parser.add_argument('-s', '--status', required=True,
                        help='Source status to pull tasks from (e.g., "Writer Doing")')
    parser.add_argument('-i', '--instructions', required=True,
                        help='Path to instruction template file (relative to workspace)')
    parser.add_argument('-f', '--finish', required=True,
                        help='Status to set after successful completion (e.g., "Writer Done")')
    parser.add_argument('--limit', type=int,
                        help='Maximum number of tasks to process')
    parser.add_argument('--no-interactive', action='store_true',
                        help='Run without user confirmation prompts')
    parser.add_argument('--workspace', type=Path,
                        help='Workspace root directory (defaults to current directory)')
    
    args = parser.parse_args()
    
    # Determine workspace root
    workspace = args.workspace or Path.cwd()
    if not workspace.exists():
        print(f"❌ Workspace directory not found: {workspace}")
        sys.exit(1)
    
    # Create and run task runner
    runner = TaskRunner(workspace)
    runner.run(
        source_status=args.status,
        instruction_template=args.instructions,
        finish_status=args.finish,
        limit=args.limit,
        interactive=not args.no_interactive
    )


if __name__ == '__main__':
    main()
