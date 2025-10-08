from .llm import LLM
from .personality import Personality

class Agent:
    def __init__(self, personality: Personality, memory, tools):
        self.llm = LLM(personality)
        self.memory = memory
        self.tools = {tool.name: tool for tool in tools}

    def run(self, user_input):
        self.memory.add_message("user", user_input)

        while True:
            response = self.llm.generate(self.memory.get_history())

            if response["type"] == "tool_call" or response["type"] == "code_patch":
                tool_name = response["tool_name"]
                tool_args = response["tool_args"]

                if tool_name in self.tools:
                    tool = self.tools[tool_name]
                    tool_output = tool.use(**tool_args)
                    self.memory.add_message("tool", tool_output)

                    # If the agent modified its own code, it should stop to reload.
                    if response["type"] == "code_patch":
                        return "I have modified my source code. Please restart me to see the changes."
                else:
                    self.memory.add_message("tool", f"Error: Tool '{tool_name}' not found.")

            elif response["type"] == "final_answer":
                final_response = response["content"]
                self.memory.add_message("assistant", final_response)
                return final_response