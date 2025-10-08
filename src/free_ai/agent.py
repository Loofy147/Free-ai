class Agent:
    def __init__(self, llm, memory, tools):
        self.llm = llm
        self.memory = memory
        self.tools = tools

    def run(self, user_input):
        self.memory.add_message("user", user_input)

        # In the future, the agent will decide which tools to use.
        # For now, it just uses the LLM to generate a response.

        response = self.llm.generate(self.memory.get_history())
        self.memory.add_message("assistant", response)

        return response