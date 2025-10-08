import os

class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, *args, **kwargs):
        raise NotImplementedError

class FileSystemTool(Tool):
    def __init__(self):
        super().__init__("FileSystemTool", "A tool for interacting with the file system. Can list_files, read_file, and write_file.")

    def use(self, operation: str, **kwargs):
        if operation == "list_files":
            return self._list_files(**kwargs)
        elif operation == "read_file":
            return self._read_file(**kwargs)
        elif operation == "write_file":
            return self._write_file(**kwargs)
        else:
            return f"Error: Unknown operation '{operation}'. Available operations: list_files, read_file, write_file."

    def _list_files(self, path: str = "."):
        try:
            files = os.listdir(path)
            return f"Files in '{path}':\n" + "\n".join(files)
        except Exception as e:
            return f"Error listing files in '{path}': {e}"

    def _read_file(self, filepath: str):
        try:
            with open(filepath, "r") as f:
                content = f.read()
            return f"Content of file '{filepath}':\n{content}"
        except Exception as e:
            return f"Error reading file '{filepath}': {e}"

    def _write_file(self, filepath: str, content: str):
        try:
            with open(filepath, "w") as f:
                f.write(content)
            return f"Successfully wrote to file '{filepath}'."
        except Exception as e:
            return f"Error writing to file '{filepath}': {e}"