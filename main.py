from src.free_ai.agent import Agent
from src.free_ai.llm import LLM
from src.free_ai.memory import Memory
from src.free_ai.tools import ExampleTool

def main():
    # Initialize the components
    llm = LLM()
    memory = Memory()
    tools = [ExampleTool()]

    # Create the agent
    agent = Agent(llm, memory, tools)

    # Run the agent with some user input
    user_input = "Hello, world!"
    response = agent.run(user_input)

    # Print the conversation
    print("User:", user_input)
    print("Agent:", response)
    print("\nMemory:")
    print(memory.get_history())

if __name__ == "__main__":
    main()