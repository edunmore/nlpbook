#!/usr/bin/env python3
"""
Batch Task Processor - Run the complete pipeline automatically

This script chains multiple task_runner.py calls to process tasks through
the entire workflow pipeline from Writer → CC → SE → QA → Finished.

Usage:
    python scripts/batch_process.py --limit 3
    python scripts/batch_process.py --no-interactive
    python scripts/batch_process.py --start-from cc
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class PipelineStage:
    """Represents a stage in the processing pipeline."""
    
    def __init__(self, name: str, source_status: str, template: str, finish_status: str):
        self.name = name
        self.source_status = source_status
        self.template = template
        self.finish_status = finish_status


class BatchProcessor:
    """Orchestrates batch processing through multiple pipeline stages."""
    
    # Define the complete pipeline
    PIPELINE = [
        PipelineStage("Writer", "Writer Doing", "prompts/WRITER_INSTRUCTIONS.md", "Writer Done"),
        PipelineStage("Character Curator", "CC Doing", "prompts/CC_INSTRUCTIONS.md", "CC Done"),
        PipelineStage("Style Editor", "SE Doing", "prompts/SE_INSTRUCTIONS.md", "SE Done"),
        PipelineStage("QA", "QA Doing", "prompts/QA_INSTRUCTIONS.md", "Finished"),
        PipelineStage("PO Review", "PO Review", "prompts/PO_INSTRUCTIONS.md", "Finished"),
    ]
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.task_runner = workspace_root / "scripts" / "task_runner.py"
        
    def run_stage(self, stage: PipelineStage, limit: Optional[int] = None,
                  interactive: bool = True) -> bool:
        """
        Run a single pipeline stage.
        
        Returns:
            True if stage completed successfully, False otherwise
        """
        print("\n" + "="*80)
        print(f"🎯 Running Stage: {stage.name}")
        print("="*80)
        
        cmd = [
            sys.executable,
            str(self.task_runner),
            "-s", stage.source_status,
            "-i", stage.template,
            "-f", stage.finish_status,
        ]
        
        if limit:
            cmd.extend(["--limit", str(limit)])
        
        if not interactive:
            cmd.append("--no-interactive")
        
        cmd.extend(["--workspace", str(self.workspace_root)])
        
        print(f"📝 Command: {' '.join(cmd)}\n")
        
        try:
            result = subprocess.run(cmd, cwd=str(self.workspace_root))
            
            if result.returncode == 0:
                print(f"\n✅ {stage.name} stage completed successfully")
                return True
            else:
                print(f"\n❌ {stage.name} stage failed with return code {result.returncode}")
                return False
                
        except Exception as e:
            print(f"\n❌ Error running {stage.name} stage: {e}")
            return False
    
    def run_pipeline(self, start_from: Optional[str] = None, limit: Optional[int] = None,
                     interactive: bool = True, stop_on_error: bool = True) -> None:
        """
        Run the complete pipeline or start from a specific stage.
        
        Args:
            start_from: Stage name to start from (e.g., 'writer', 'cc', 'se', 'qa', 'po')
            limit: Maximum number of tasks per stage
            interactive: Whether to run in interactive mode
            stop_on_error: Stop pipeline if a stage fails
        """
        print("\n" + "="*80)
        print("📚 Batch Task Processor - Complete Pipeline")
        print("="*80)
        print(f"Workspace: {self.workspace_root}")
        print(f"Limit per stage: {limit if limit else 'No limit'}")
        print(f"Interactive: {'Yes' if interactive else 'No'}")
        print(f"Stop on error: {'Yes' if stop_on_error else 'No'}")
        
        # Find starting stage
        start_idx = 0
        if start_from:
            start_from_lower = start_from.lower()
            stage_map = {
                'writer': 0,
                'cc': 1,
                'character': 1,
                'se': 2,
                'style': 2,
                'qa': 3,
                'po': 4,
            }
            start_idx = stage_map.get(start_from_lower, 0)
            print(f"Starting from: {self.PIPELINE[start_idx].name}")
        
        print("="*80 + "\n")
        
        # Run pipeline stages
        stages_to_run = self.PIPELINE[start_idx:]
        total_stages = len(stages_to_run)
        completed = 0
        failed = 0
        
        for idx, stage in enumerate(stages_to_run, 1):
            print(f"\n{'─'*80}")
            print(f"Stage {idx}/{total_stages}")
            print(f"{'─'*80}")
            
            if interactive:
                response = input(f"Run {stage.name} stage? [Y/n/q]: ").strip().lower()
                if response == 'q':
                    print("🛑 Pipeline stopped by user")
                    break
                if response == 'n':
                    print("⏭️  Skipped")
                    continue
            
            success = self.run_stage(stage, limit=limit, interactive=interactive)
            
            if success:
                completed += 1
            else:
                failed += 1
                if stop_on_error:
                    print(f"\n⚠️  Stopping pipeline due to error in {stage.name} stage")
                    break
        
        # Summary
        print("\n" + "="*80)
        print("📊 Pipeline Summary")
        print("="*80)
        print(f"Total stages: {total_stages}")
        print(f"✅ Completed: {completed}")
        print(f"❌ Failed: {failed}")
        print(f"⏭️  Skipped: {total_stages - completed - failed}")
        print("="*80 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Run batch processing through the complete pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete pipeline interactively
  python scripts/batch_process.py
  
  # Run complete pipeline with limit of 3 tasks per stage
  python scripts/batch_process.py --limit 3
  
  # Run fully automated (no prompts)
  python scripts/batch_process.py --no-interactive
  
  # Start from Character Curator stage
  python scripts/batch_process.py --start-from cc
  
  # Continue on errors (don't stop)
  python scripts/batch_process.py --no-stop-on-error
        """
    )
    
    parser.add_argument('--limit', type=int,
                        help='Maximum number of tasks to process per stage')
    parser.add_argument('--no-interactive', action='store_true',
                        help='Run without user confirmation prompts')
    parser.add_argument('--start-from', type=str,
                        choices=['writer', 'cc', 'character', 'se', 'style', 'qa', 'po'],
                        help='Start from a specific stage')
    parser.add_argument('--no-stop-on-error', action='store_true',
                        help='Continue pipeline even if a stage fails')
    parser.add_argument('--workspace', type=Path,
                        help='Workspace root directory (defaults to current directory)')
    
    args = parser.parse_args()
    
    # Determine workspace root
    workspace = args.workspace or Path.cwd()
    if not workspace.exists():
        print(f"❌ Workspace directory not found: {workspace}")
        sys.exit(1)
    
    # Check if task_runner.py exists
    task_runner = workspace / "scripts" / "task_runner.py"
    if not task_runner.exists():
        print(f"❌ task_runner.py not found: {task_runner}")
        print("   Make sure you're running this from the workspace root.")
        sys.exit(1)
    
    # Create and run batch processor
    processor = BatchProcessor(workspace)
    processor.run_pipeline(
        start_from=args.start_from,
        limit=args.limit,
        interactive=not args.no_interactive,
        stop_on_error=not args.no_stop_on_error
    )


if __name__ == '__main__':
    main()
