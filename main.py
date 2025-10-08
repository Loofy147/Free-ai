import os
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

    # --- Test Scenario ---
    test_filepath = "test_file.txt"
    test_content = "This is a test file created by the Free-ai agent."

    prompts = [
        f"write to file '{test_filepath}' with content: {test_content}",
        "Can you list files now?",
        f"Please read file '{test_filepath}'"
    ]

    for user_input in prompts:
        print(f"--- User: {user_input} ---")
        response = agent.run(user_input)
        print(f"Agent: {response}\n")

    print("--- Final Memory ---")
    import json
    print(json.dumps(memory.get_history(), indent=2))

    # --- Cleanup ---
    if os.path.exists(test_filepath):
        os.remove(test_filepath)
        print(f"\nCleaned up {test_filepath}.")


if __name__ == "__main__":
    main()