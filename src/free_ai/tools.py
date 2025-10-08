import os

class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, *args, **kwargs):
        raise NotImplementedError

class FileSystemTool(Tool):
    def __init__(self):
        super().__init__(
            "FileSystemTool",
            "A tool for interacting with the file system."
        )

    def use(self, operation: str, **kwargs):
        if operation == "read_file":
            return self._read_file(**kwargs)
        elif operation == "write_file":
            return self._write_file(**kwargs)
        elif operation == "modify_file":
            return self._modify_file(**kwargs)
        else:
            return f"Error: Unknown operation '{operation}'. Supported: read_file, write_file, modify_file."

    def _read_file(self, filepath: str):
        """Reads the content of a specified file."""
        try:
            with open(filepath, "r") as f:
                content = f.read()
            return f"Content of '{filepath}':\n---\n{content}\n---"
        except FileNotFoundError:
            return f"Error: File not found at '{filepath}'."
        except Exception as e:
            return f"Error reading file '{filepath}': {type(e).__name__}: {e}"

    def _write_file(self, filepath: str, content: str):
        """Writes content to a specified file."""
        try:
            with open(filepath, "w") as f:
                f.write(content)
            return f"Successfully wrote to file '{filepath}'."
        except Exception as e:
            return f"Error writing to file '{filepath}': {type(e).__name__}: {e}"

    def _modify_file(self, filepath: str, content_to_append: str):
        """Appends content to a specified file."""
        try:
            with open(filepath, "a") as f:
                f.write(content_to_append)
            return f"Successfully modified file '{filepath}'."
        except Exception as e:
            return f"Error modifying file '{filepath}': {type(e).__name__}: {e}"
