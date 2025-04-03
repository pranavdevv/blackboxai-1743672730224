import subprocess
import os
import resource
import time
import json
from pathlib import Path

def execute_python_code(code, input_data=None, timeout=5):
    """
    Execute Python code in a secure Docker container
    Returns: (success, output, execution_time, memory_usage)
    """
    # Create temp directory
    temp_dir = Path('/tmp/code_execution')
    temp_dir.mkdir(exist_ok=True)
    
    # Write code to file
    code_file = temp_dir / 'solution.py'
    with open(code_file, 'w') as f:
        f.write(code)
    
    # Prepare Docker command
    docker_cmd = [
        'docker', 'run', '--rm',
        '-v', f'{temp_dir}:/code',
        '-w', '/code',
        'python:3.9-slim',
        'timeout', str(timeout), 'python', 'solution.py'
    ]
    
    try:
        start_time = time.time()
        process = subprocess.Popen(
            docker_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE if input_data else None,
            text=True
        )
        
        stdout, stderr = process.communicate(
            input=input_data if input_data else None
        )
        execution_time = time.time() - start_time
        
        if process.returncode == 124:  # Timeout
            return False, "Execution timed out", execution_time, 0
        elif process.returncode != 0:
            return False, stderr or "Runtime error", execution_time, 0
            
        return True, stdout, execution_time, 0
        
    except Exception as e:
        return False, str(e), 0, 0
    finally:
        # Clean up
        try:
            code_file.unlink()
        except:
            pass