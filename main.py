from src.free_ai.agent import Agent
from src.free_ai.llm import LLM
from src.free_ai.memory import Memory
from src.free_ai.tools import FileSystemTool

def main():
    # Initialize the components
    llm = LLM()
    memory = Memory()
    tools = [FileSystemTool()]

    # Create the agent
    agent = Agent(llm, memory, tools)

    # Run the agent with some user input that should trigger a tool call
    user_input = "Can you list files in the current directory?"
    response = agent.run(user_input)

    # Print the conversation
    print("User:", user_input)
    print("Agent:", response)
    print("\nMemory:")
    print(memory.get_history())

if __name__ == "__main__":
    main()