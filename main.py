import json
from src.free_ai.agent import Director
from src.free_ai.personality import WhimsicalPersonality

# --- The Body's External Tools ---
# For this challenge, the agent is performing an internal refactoring.
# It does not require any external tools from the Body.
BODY_TOOLS = {}

# --- The Main Execution Loop (The ExecutorBody) ---

def main():
    print("--- Project Ascension: The ExecutorBody is awakening... ---")

    # 1. The Body instantiates the Director with a chosen personality.
    personality = WhimsicalPersonality()
    director = Director(personality)
    history = []

    # 2. Define the high-level goal for the Ascension Challenge.
    goal = "Refactor your `FileSystemTool` to add a new `modify_file` operation that appends text to a file."
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

            if tool_name in BODY_TOOLS:
                tool_function = BODY_TOOLS[tool_name]
                result = tool_function(**arguments)
            elif tool_name in director.tools:
                # The Director's tools can be functions or class instances.
                tool = director.tools[tool_name]
                if hasattr(tool, 'use'): # It's a tool instance.
                    result = tool.use(**arguments)
                else: # It's a direct function call.
                    result = tool(**arguments)
            else:
                result = f"Error: Tool '{tool_name}' not found."

            print(f"BODY: Tool '{tool_name}' executed. Result:\n---\n{result}\n---\n")
            history.append({"role": "body", "action_taken": action, "result": result})

        else:
            print(f"BODY: Error - The Director proposed an unknown action type: '{action_type}'")
            break

        # c. The Body checks for failure before continuing.
        # This is a more robust check that looks for a structured error response.
        error_found = False
        if isinstance(result, dict) and result.get("status") == "error":
            error_found = True

        if error_found:
            print(f"BODY: A critical error was detected. Halting the plan. Reason: {result.get('message')}")
            break

    print("--- Project Ascension: The Body's work is done. ---")

if __name__ == "__main__":
    main()