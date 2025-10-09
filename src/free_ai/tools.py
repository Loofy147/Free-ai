import os

class Tool:
    """An abstract base class for all agent tools.

    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of what the tool does.
    """
    def __init__(self, name: str, description: str):
        """Initializes the Tool.

        Args:
            name (str): The name of the tool.
            description (str): A description of the tool's purpose.
        """
        self.name = name
        self.description = description

    def use(self, *args, **kwargs):
        """The main method to execute the tool's functionality.

        This method must be overridden by any concrete tool implementation.

        Raises:
            NotImplementedError: If the method is not overridden.
        """
        raise NotImplementedError

class FileSystemTool(Tool):
    """A tool for interacting with the local file system."""
    def __init__(self):
        """Initializes the FileSystemTool."""
        super().__init__(
            "FileSystemTool",
            "A tool for interacting with the file system, capable of reading, writing, and modifying files."
        )

    def use(self, operation: str, **kwargs) -> dict:
        """Dispatches file operations based on the provided command.

        Args:
            operation (str): The file operation to perform. Supported values
                are "read_file", "write_file", and "modify_file".
            **kwargs: The arguments required for the specific operation.

        Returns:
            dict: A dictionary containing the status and result of the
                operation.
        """
        if operation == "read_file":
            return self._read_file(**kwargs)
        elif operation == "write_file":
            return self._write_file(**kwargs)
        elif operation == "modify_file":
            return self._modify_file(**kwargs)
        else:
            return {"status": "error", "message": f"Unknown operation '{operation}'. Supported: read_file, write_file, modify_file."}

    def _read_file(self, filepath: str) -> dict:
        """Reads the entire content of a specified file.

        Args:
            filepath (str): The path to the file to be read.

        Returns:
            dict: A dictionary containing the status and, on success, the
                file's content.
        """
        try:
            with open(filepath, "r") as f:
                content = f.read()
            return {"status": "success", "content": f"Content of '{filepath}':\n---\n{content}\n---"}
        except FileNotFoundError:
            return {"status": "error", "message": f"File not found at '{filepath}'."}
        except Exception as e:
            return {"status": "error", "message": f"Error reading file '{filepath}': {type(e).__name__}: {e}"}

    def _write_file(self, filepath: str, content: str) -> dict:
        """Writes content to a file, overwriting it if it exists.

        Args:
            filepath (str): The path to the file to be written to.
            content (str): The content to write to the file.

        Returns:
            dict: A dictionary containing the status of the write operation.
        """
        try:
            with open(filepath, "w") as f:
                f.write(content)
            return {"status": "success", "message": f"Successfully wrote to file '{filepath}'."}
        except Exception as e:
            return {"status": "error", "message": f"Error writing to file '{filepath}': {type(e).__name__}: {e}"}

    def _modify_file(self, filepath: str, content_to_append: str) -> dict:
        """Appends content to the end of a specified file.

        Args:
            filepath (str): The path to the file to be modified.
            content_to_append (str): The content to append to the file.

        Returns:
            dict: A dictionary containing the status of the append operation.
        """
        try:
            with open(filepath, "a") as f:
                f.write(content_to_append)
            return {"status": "success", "message": f"Successfully modified file '{filepath}'."}
        except Exception as e:
            return {"status": "error", "message": f"Error modifying file '{filepath}': {type(e).__name__}: {e}"}