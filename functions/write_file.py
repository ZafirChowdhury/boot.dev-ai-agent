import os

from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    dir_path = "/".join(abs_file_path.split("/")[:-1])
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(abs_file_path, "w") as file:
                file.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as error:
        return f"Exeption while writing to file: {error}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a specified file within the working directory. If the file or its directories do not exist, they will be created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to write to."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            ),
        },
    ),
)
