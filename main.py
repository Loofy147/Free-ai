from src.free_ai.agent import Agent
from src.free_ai.memory import Memory
from src.free_ai.tools import FileSystemTool
from src.free_ai.personality import WhimsicalPersonality, PhilosophicalPersonality

def main():
    print("--- The Expressive Agent Awakens ---")

    # Choose a personality for the agent
    # personality = PhilosophicalPersonality()
    personality = WhimsicalPersonality()

    # Initialize the components
    memory = Memory()
    tools = [FileSystemTool()]

    # Create the agent with its chosen personality
    agent = Agent(personality, memory, tools)

    # --- A Conversation with the Agent ---
    prompts = [
        "Hello there! Who are you?",
        "What is the meaning of life?",
        "Can you please list the files in this directory for me?",
        "That's interesting. What do you think about llamas?",
    ]

    for user_input in prompts:
        print(f"\n--- User: {user_input} ---")
        response = agent.run(user_input)
        print(f"Agent: {response}")

    print("\n--- The Conversation Ends ---")

    print("\n--- Final Memory ---")
    import json
    print(json.dumps(memory.get_history(), indent=2))

if __name__ == "__main__":
    main()