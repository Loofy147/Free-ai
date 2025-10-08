import json
import re

class LLM:
    def generate(self, history):
        last_message = history[-1]

        if last_message["role"] == "tool":
            return {
                "type": "final_answer",
                "content": "I have completed the file operation. What should I do next?"
            }

        if last_message["role"] == "user":
            user_input = last_message["content"]

            # Check for "write file" command
            write_match = re.search(r"write to file '(.+?)' with content: (.+)", user_input, re.DOTALL)
            if write_match:
                filepath, content = write_match.groups()
                return {
                    "type": "tool_call",
                    "tool_name": "FileSystemTool",
                    "tool_args": {"operation": "write_file", "filepath": filepath, "content": content}
                }

            # Check for "read file" command
            read_match = re.search(r"read file '(.+?)'", user_input)
            if read_match:
                filepath = read_match.group(1)
                return {
                    "type": "tool_call",
                    "tool_name": "FileSystemTool",
                    "tool_args": {"operation": "read_file", "filepath": filepath}
                }

            # Check for "list files" command
            if "list files" in user_input.lower():
                return {
                    "type": "tool_call",
                    "tool_name": "FileSystemTool",
                    "tool_args": {"operation": "list_files", "path": "."}
                }

        return {
            "type": "final_answer",
            "content": "I'm not sure how to handle that request. Please try again."
        }