import subprocess
import os
import datetime
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

def load_prompt(world_dir, filename):
    """
    Load prompt with override logic:
    1. worlds/{world}/prompts/{filename}
    2. prompts/{filename} (Global fallback)
    """
    # 1. World Override
    if world_dir:
        world_prompt = world_dir / "prompts" / filename
        if world_prompt.exists():
            print(f"Loaded world prompt: {world_prompt}")
            try:
                with open(world_prompt, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"Error loading world prompt {filename}: {e}")

    # 2. Global Default
    global_prompt = WORKSPACE_ROOT / "prompts" / filename
    if global_prompt.exists():
        print(f"Loaded global prompt: {global_prompt}")
        try:
            with open(global_prompt, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error loading global prompt {filename}: {e}")
            
    print(f"Warning: Prompt {filename} not found.")
    return ""

def run_agent(prompt, model="gemini", world_dir=None, task_name="agent_task", cwd=None):
    """
    Runs the agent command and logs interaction history if world_dir is provided.
    """
    print(f"Running agent for task: {task_name}...")
    if cwd:
        print(f"  Working Directory: {cwd}")
    
    cmd = [model, "-p", prompt]
    start_time = datetime.datetime.now()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=cwd)
        output = result.stdout
        
        # Log History if world_dir is provided
        if world_dir:
            try:
                history_dir = world_dir / "history"
                os.makedirs(history_dir, exist_ok=True)
                
                timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{timestamp}_{task_name}.md"
                log_path = history_dir / filename
                
                log_content = f"""# Interaction History: {task_name}
**Date:** {start_time.strftime("%Y-%m-%d %H:%M:%S")}
**Model:** {model}

## Prompt
```text
{prompt}
```

## Output
{output}
"""
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write(log_content)
                    
                print(f"Logged interaction to {log_path}")
                
            except Exception as e:
                print(f"Warning: Failed to log history: {e}")
                
        return output
        
    except subprocess.CalledProcessError as e:
        print(f"Error running agent: {e}")
        print(f"Stderr: {e.stderr}")
        return None
