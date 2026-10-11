import os

MAX_CHARS = 10000
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a specified file up to MAX_CHARS",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file we want to read, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_path, file_path))
        # Will be True or False
        valid_target_file = os.path.commonpath([abs_working_path, target_file]) == abs_working_path
        if valid_target_file == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        print(f'Success: "{file_path}" is within the working directory')
        if os.path.isfile(os.path.abspath(target_file)) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # validation successful; now, actually do something
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

    except Exception as e:
        print(f"Error: {e}")
