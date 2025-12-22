import subprocess
import os
import datetime
import sys
from pathlib import Path

def run_agent(prompt, model="gemini", world_dir=None, task_name="agent_task"):
    """
    Runs the agent command and logs interaction history if world_dir is provided.
    """
    print(f"Running agent for task: {task_name}...")
    
    cmd = [model, "-p", prompt]
    start_time = datetime.datetime.now()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
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
