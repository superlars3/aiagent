import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_target.startswith(abs_working):
        return f'Result for "{directory}" directory: \n    Error: Cannot list "{directory}" as it is outside the permitted working directory\n'

    if os.path.isdir(abs_target) == False:
        return f'Result for "{directory}" directory: \n    Error: "{directory}" is not a directory\n'

    file_list = os.listdir(abs_target)
    string_list = []
    for file in file_list:
        file_path = os.path.join(abs_target, file)
        string_list.append(f'- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}')
    final = "\n ".join(string_list)
    return f"Result for {directory}: \n    {final} \n"
