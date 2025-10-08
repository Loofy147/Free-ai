import json

class LLM:
    def generate(self, history):
        # In the future, this will call a real LLM API.
        # For now, it returns a mock response that can simulate a tool call.

        last_message = history[-1]

        # If the last message is from a tool, generate a final answer.
        if last_message["role"] == "tool":
            return {
                "type": "final_answer",
                "content": f"Okay, I have the file list. The final answer is based on this tool output."
            }

        # If the last message is from the user, decide whether to call a tool.
        if last_message["role"] == "user":
            user_input = last_message["content"]
            if "list files" in user_input.lower():
                # Simulate a tool call
                return {
                    "type": "tool_call",
                    "tool_name": "FileSystemTool",
                    "tool_args": {"path": "."}
                }

        # Default to a final answer if no other condition is met.
        return {
            "type": "final_answer",
            "content": "This is a mock response from the LLM."
        }