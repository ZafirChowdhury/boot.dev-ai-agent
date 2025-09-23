import os

def get_files_info(working_directory, directory="."):
    output_str = f"Result for {"current" if directory == "." else directory} directory:" + "\n"

    if directory.startswith("/"):
        output_str += f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return output_str
    
    if len(directory) >= 2:
        if directory[0] == "." and (directory[1] == "." or directory[1] == "/"):
            output_str += f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            return output_str
    
    full_reletive_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_reletive_path)

    if not os.path.isdir(abs_path):
        output_str += f'Error: "{directory}" is not a directory'
        return output_str
    
    list_dir = os.listdir(abs_path)
    for file_name in list_dir:
        file_path = os.path.join(abs_path, file_name)
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        output_str += f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}" + "\n"

    return output_str
