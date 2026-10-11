import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_path, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_path, target_dir]) == abs_working_path
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        print(f'Success: "{directory}" is within the working directory')
        if os.path.isdir(os.path.abspath(target_dir)) == False:
            return f'Error: "{target_dir}" is not a directory'
        # validation successful; now, actually do something
        content_string = ""
        for file in os.listdir(target_dir):
            path = os.path.abspath(f"{target_dir}/{file}")
            content_string += f"- {file}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}\n"
        return content_string

    except Exception as e:
        print(f"Error: {e}")
