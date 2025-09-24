import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        subprocess_args = ["python3", abs_file_path] + args

        completed_process = subprocess.run(subprocess_args, capture_output=True, text=True, timeout=30)
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
            
        return f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}"

    except Exception as error:
        return f"Error: executing Python file: {error}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its standard output and standard error.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the Python file to execute."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the script.",
            ),
        },
    ),
)