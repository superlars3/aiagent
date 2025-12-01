import os
from .config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="reads the contents of a file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the contents from, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    file_target = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_target.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'
    if os.path.isfile(file_target) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"\n'


    try:
        with open(file_target, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(file_target) > MAX_CHARS:
                full_string = file_content_string + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]\n'
                return full_string
        return file_content_string
    except Exception as e:
        return f'Error: {e}\n'
