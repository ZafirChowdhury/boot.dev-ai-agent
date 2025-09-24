import os

from google.genai import types

def get_files_info(working_directory, directory="."):
    output_str = f"Result for {"current" if directory == "." else directory} directory:" + "\n"

    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_dir.startswith(abs_working_dir):
        output_str += f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return output_str

    if not os.path.isdir(abs_dir):
        output_str += f'Error: "{directory}" is not a directory'
        return output_str
    
    list_dir = os.listdir(abs_dir)
    for file_name in list_dir:
        file_path = os.path.join(abs_dir, file_name)
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        output_str += f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}" + "\n"

    return output_str


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
