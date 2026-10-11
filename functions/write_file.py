import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes 'content' to the specified file at 'file_path'",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file we want to write, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "The content we will write to the file",
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_path, file_path))
        # Will be True or False
        valid_target_file = os.path.commonpath([abs_working_path, target_file]) == abs_working_path
        if valid_target_file == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        print(f'Success: "{file_path}" is within the working directory')
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(abs_working_path, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return(f"Error: {e}")
