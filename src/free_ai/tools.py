import os

class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, *args, **kwargs):
        raise NotImplementedError

class FileSystemTool(Tool):
    def __init__(self):
        super().__init__("FileSystemTool", "A tool for listing files in the current directory.")

    def use(self):
        try:
            files = os.listdir(".")
            return "Files in the current directory:\n" + "\n".join(files)
        except Exception as e:
            return f"Error listing files: {e}"