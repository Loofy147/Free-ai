import json
from src.free_ai.agent import Director
from src.free_ai.personality import WhimsicalPersonality

# --- The Body's External Tools ---
# These are functions that the Body can execute.
# In a real environment, these would be calls to powerful, external APIs.

def final_answer(answer: str) -> str:
    """A tool to provide the final answer and terminate the process."""
    return f"Final Answer: {answer}"

BODY_TOOLS = {
    "final_answer": final_answer,
}

# --- The Main Execution Loop (The ExecutorBody) ---

def main():
    print("--- Project Oracle: The ExecutorBody is awakening... ---")

    # 1. The Body instantiates the Director with a chosen personality.
    personality = WhimsicalPersonality()
    director = Director(personality)
    history = []

    # 2. Define the high-level goal for the Oracle Quest.
    goal = "Know Thyself. Analyze your own source code to find your greatest limitation and design the solution."
    print(f"BODY: Received goal: {goal}\n")
    history.append({"role": "system", "content": f"The goal is: {goal}"})

    # 3. The Body enters the main loop, driven by the Director's decisions.
    for i in range(10): # Add a safety break to prevent infinite loops.
        # a. Get the next intended action from the Director.
        action = director.determine_next_action(goal, history)

        action_type = action.get("action")
        print(f"DIRECTOR proposes action: {action_type}")

        if action_type == "finish":
            print(f"BODY: The Director has finished its plan. Reason: {action.get('reason')}")
            break

        # b. The Body executes the action.
        result = None
        if action_type == "express_personality":
            context = action.get("arguments", {}).get("context", "")
            result = personality.express(context=context)
            print(f"BODY (expressing personality): {result}\n")
            history.append({"role": "assistant", "content": result})

        elif action_type == "use_tool":
            tool_name = action.get("tool_name")
            arguments = action.get("arguments", {})

            print(f"BODY: Preparing to use tool '{tool_name}'...")

            # Check if it's a tool the Body provides directly.
            if tool_name in BODY_TOOLS:
                tool_function = BODY_TOOLS[tool_name]
                result = tool_function(**arguments)
            # Check if it's an internal tool the Director knows about.
            elif tool_name in director.tools:
                tool_instance = director.tools[tool_name]
                result = tool_instance.use(**arguments)
            else:
                result = f"Error: Tool '{tool_name}' not found."

            print(f"BODY: Tool '{tool_name}' executed. Result:\n---\n{result}\n---\n")
            history.append({"role": "body", "action_taken": action, "result": result})

        else:
            print(f"BODY: Error - The Director proposed an unknown action type: '{action_type}'")
            break

        # c. The Body checks for failure before continuing.
        error_found = False
        if isinstance(result, str) and "Error:" in result:
            error_found = True

        if error_found:
            print("BODY: A critical error was detected. Halting the current plan.")
            break

        # d. If the final answer is given, the work is done.
        if action_type == "use_tool" and tool_name == "final_answer":
            break

    print("--- Project Oracle: The Body's work is done. ---")

if __name__ == "__main__":
    main()