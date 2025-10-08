class Agent:
    def __init__(self, llm, memory, tools):
        self.llm = llm
        self.memory = memory
        self.tools = {tool.name: tool for tool in tools}

    def run(self, user_input):
        self.memory.add_message("user", user_input)

        while True:
            response = self.llm.generate(self.memory.get_history())

            if response["type"] == "tool_call":
                tool_name = response["tool_name"]
                tool_args = response["tool_args"]

                if tool_name in self.tools:
                    tool = self.tools[tool_name]
                    tool_output = tool.use(**tool_args)
                    self.memory.add_message("tool", tool_output)
                else:
                    self.memory.add_message("tool", f"Error: Tool '{tool_name}' not found.")

            elif response["type"] == "final_answer":
                final_response = response["content"]
                self.memory.add_message("assistant", final_response)
                return final_response