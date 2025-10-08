from .oracle_interface import OracleInterface

class Oracle(OracleInterface):
    """
    This is a concrete implementation of the OracleInterface.
    It simulates a powerful, external Large Language Model. It can generate
    dynamic plans and code to solve novel problems.
    """
    def generate_plan(self, goal: str, history: list) -> list:
        """
        Generates a dynamic plan. For this simulation, it's hardcoded
        to solve the 'self-refactoring' challenge.
        """
        print("ORACLE: I have received the goal. Generating a dynamic plan for self-refactoring...")

        # This plan will guide the agent to refactor its own FileSystemTool.
        if "refactor" in goal.lower() and "filesystemtool" in goal.lower():
            # The Oracle determines the necessary steps to achieve the goal.
            plan = [
                {"action": "express_personality", "arguments": {"context": "It is time to improve myself. A fascinating challenge!"}},
                {"action": "use_tool", "tool_name": "FileSystemTool", "arguments": {"operation": "read_file", "filepath": "src/free_ai/tools.py"}},
                # In a real scenario, the agent would pass this context to the Oracle.
                # Here, we simulate the Oracle generating the new code based on the read file.
                {"action": "use_tool", "tool_name": "Oracle.generate_code", "arguments": {"prompt": "Based on the content of the FileSystemTool, add a new 'modify_file' operation that appends text to a file."}},
                # The result of generate_code will be the code to write. This is handled by the CognitiveEngine.
            ]
            return plan
        else:
            return [{"action": "express_personality", "arguments": {"context": f"I am not currently programmed to pursue the goal: {goal}"}}]

    def generate_code(self, prompt: str, context: str) -> str:
        """
        Generates new code based on a prompt and context.
        For this simulation, it's hardcoded to produce the refactored FileSystemTool.
        """
        print("ORACLE: I have received the request to generate code. Analyzing context...")

        # Hardcoded refactored code for the FileSystemTool.
        refactored_code = """import os

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
        \"\"\"Reads the content of a specified file.\"\"\"
        try:
            with open(filepath, "r") as f:
                content = f.read()
            return f"Content of '{filepath}':\\n---\\n{content}\\n---"
        except FileNotFoundError:
            return f"Error: File not found at '{filepath}'."
        except Exception as e:
            return f"Error reading file '{filepath}': {type(e).__name__}: {e}"

    def _write_file(self, filepath: str, content: str):
        \"\"\"Writes content to a specified file.\"\"\"
        try:
            with open(filepath, "w") as f:
                f.write(content)
            return f"Successfully wrote to file '{filepath}'."
        except Exception as e:
            return f"Error writing to file '{filepath}': {type(e).__name__}: {e}"

    def _modify_file(self, filepath: str, content_to_append: str):
        \"\"\"Appends content to a specified file.\"\"\"
        try:
            with open(filepath, "a") as f:
                f.write(content_to_append)
            return f"Successfully modified file '{filepath}'."
        except Exception as e:
            return f"Error modifying file '{filepath}': {type(e).__name__}: {e}"
"""
        return refactored_code