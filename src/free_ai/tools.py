import os

class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, *args, **kwargs):
        raise NotImplementedError

class FileSystemTool(Tool):
    def __init__(self):
        super().__init__("FileSystemTool", "A tool for interacting with the file system.")

    def use(self, path="."):
        try:
            return f"Files in '{path}':\n" + "\n".join(os.listdir(path))
        except Exception as e:
            return f"Error listing files: {e}"