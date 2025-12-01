import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes the content to the file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the provided file_path",
            )
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    file_target = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_target.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if os.path.exists(file_target) == False:
            os.makedirs(os.path.dirname(file_target), exist_ok=True)
        with open(file_target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

