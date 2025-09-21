import os

def get_files_info(working_directory, directory="."):
    if directory.startswith("/"):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if len(directory) >= 2:
        if directory[0] == "." and (directory[1] == "." or directory[1] == "/"):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    full_reletive_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_reletive_path)

    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    
    list_dir = os.listdir(abs_path)
    for file_name in list_dir:
        file_path = os.path.join(abs_path, file_name)
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        print(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")

    return ""
