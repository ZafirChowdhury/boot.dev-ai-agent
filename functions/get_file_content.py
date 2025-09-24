import os

from google.genai import types

from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
    except Exception as error:
        return f"Exeption reading file: {error}"

    if len(file_content_string) == MAX_CHARS:
        return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file from the working directory. Content is truncated if it exceeds a certain size.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to read."
            ),
        },
    ),
)
