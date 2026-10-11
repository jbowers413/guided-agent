import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the specified file at 'file_path' with optional 'args'",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file we want to run, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list[str] | None",
                    "description": "The optional args we will use to run the file. Defaults to None",
                }
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_path, file_path))
        # Will be True or False
        valid_target_file = os.path.commonpath([abs_working_path, target_file]) == abs_working_path
        if valid_target_file == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # print(f'Success: "{file_path}" is within the working directory')
        if os.path.isfile(os.path.abspath(target_file)) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file'
        # OKAY we're validated, let's do some work!
        command = ["python", target_file]
        if args:
            command.extend(args)

        process_complete = subprocess.run(args=command, capture_output=True, text=True, timeout=30, check=True)
        output_string = ""
        if process_complete.returncode != 0:
            output_string += f"Process exited with code {process_complete.returncode}\n"
        if process_complete.stderr == None and process_complete.stdout == None:
            output_string += "No output produced\n"
        else:
            output_string += f"STDOUT: {process_complete.stdout}\nSTDERR: {process_complete.stderr}\n"

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
