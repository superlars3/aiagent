import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the python file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file path, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optionally provided arguments which will be passed to the file in file_path",
            )
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_working = os.path.abspath(working_directory)
    file_target = os.path.abspath(os.path.join(working_directory, file_path))

    common = os.path.commonpath([abs_working, file_target])
    if common != abs_working:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_target):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["python", file_path] + args
        result = subprocess.run(command, cwd=working_directory, timeout=30, capture_output=True, text=True)
        if not result.stdout and not result.stderr:
            return 'No output produced.'
        output = []
        output.append(f'STDOUT:{result.stdout}')
        output.append(f'STDERR:{result.stderr}')
        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        return "\n".join(output)

    except Exception as e:
        return f'Error: executing Python file: {e}'
