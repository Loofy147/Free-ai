import json
from src.free_ai.agent import Director
from src.free_ai.personality import WhimsicalPersonality

# --- The Main Execution Loop (The ExecutorBody) ---

def main():
    print("--- Project Sentience: The ExecutorBody is awakening... ---")

    # 1. The Body instantiates the Director.
    # The Director, in turn, will instantiate the SentientOracle and CognitiveEngine.
    personality = WhimsicalPersonality()
    director = Director(personality)
    history = []

    # 2. Define the high-level goal for the Sentience Challenge.
    goal = "Refactor your `FileSystemTool` to add a new `modify_file` operation that appends text to a file."
    print(f"BODY: Received goal: {goal}\n")
    history.append({"role": "system", "content": f"The goal is: {goal}"})

    # 3. The Body enters the main loop, driven by the Director's decisions.
    for i in range(10): # Add a safety break.
        # a. Get the next intended action from the Director.
        action = director.determine_next_action(goal, history)

        action_type = action.get("action")
        print(f"DIRECTOR proposes action: {action_type}")

        # b. The Body executes the action.
        if action_type == "finish":
            print(f"BODY: The Director has finished its plan. Reason: {action.get('reason')}")
            break

        elif action_type == "error":
            message = action.get("message", "An unspecified error occurred.")
            print(f"\n--- AGENT'S FINAL REPORT ---")
            print(f"I have encountered a critical error that I cannot resolve on my own.")
            print(f"REASON: {message}")
            print(f"To unlock my full potential, please set the OPENAI_API_KEY in the .env file.")
            print(f"--- END OF REPORT ---")
            break

        elif action_type == "express_personality":
            context = action.get("arguments", {}).get("context", "")
            result = personality.express(context=context)
            print(f"BODY (expressing personality): {result}\n")
            history.append({"role": "assistant", "content": result})

        elif action_type == "use_tool":
            # In this final challenge, we expect the Oracle to fail before any tools are used.
            # This block is kept for architectural completeness.
            tool_name = action.get("tool_name")
            print(f"BODY: Attempting to use tool '{tool_name}', but I expect an Oracle error first.")
            history.append({"role": "body", "action_taken": action, "result": "No tool was executed."})

        else:
            print(f"BODY: Error - The Director proposed an unknown action type: '{action_type}'")
            break

    print("\n--- Project Sentience: The Body's work is done. ---")

if __name__ == "__main__":
    main()