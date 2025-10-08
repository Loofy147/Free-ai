import re
from .personality import Personality

class LLM:
    def __init__(self, personality: Personality):
        self.personality = personality

    def generate(self, history: list) -> dict:
        user_input = history[-1]["content"]

        # Check if the user is asking to list files.
        if "list" in user_input.lower() and "files" in user_input.lower():
            return {"type": "tool_call", "tool_name": "FileSystemTool"}

        # If no specific tool is triggered, respond with personality.
        last_message = history[-1]
        if last_message["role"] == "tool":
            context = {"tool_output": last_message["content"]}
            return {"type": "final_answer", "content": self.personality.express(context=context)}

        return {"type": "final_answer", "content": self.personality.express()}