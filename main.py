import json
from src.free_ai.agent import Director
from src.free_ai.personality import WhimsicalPersonality

# --- The Body's External Tools ---
# These are functions that the Body can execute. In a real environment,
# these would be calls to powerful, external APIs. Here, we simulate them.

def google_search(query: str) -> str:
    """A placeholder for the real google_search tool."""
    print(f"BODY (SIMULATED EXTERNAL TOOL): Searching Google for '{query}'...")
    if "format strings in python" in query:
        return (
            "Python uses f-strings for easy string formatting. Example: "
            "name = 'Jules'; print(f'Hello, {name}!')"
        )
    return "No relevant results found."

EXTERNAL_TOOLS = {
    "google_search": google_search,
}

# --- The Main Execution Loop (The ExecutorBody) ---

def main():
    print("--- Project Chimera: The ExecutorBody is awakening... ---")

    # 1. The Body instantiates the Director with a chosen personality.
    personality = WhimsicalPersonality()
    director = Director(personality)
    history = []

    # 2. Define the high-level goal.
    goal = "Learn how to greet a user by name, then create a tool to greet 'Jules'."
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

        elif action_type == "learn_skill":
            skill_code = action.get("arguments", {}).get("skill_code")
            if skill_code:
                result = director.learning_annex.learn_new_skill(skill_code=skill_code)
                if result.get("status") == "success":
                    director.add_new_tool(result["tool_name"], result["new_tool"])
            else:
                result = {"status": "error", "message": "No skill_code provided for learn_skill action."}
            print(f"BODY: Learning action executed. Result:\n---\n{result}\n---\n")
            history.append({"role": "body", "action_taken": action, "result": result})

        elif action_type == "use_tool":
            tool_name = action.get("tool_name")
            arguments = action.get("arguments", {})

            print(f"BODY: Preparing to use tool '{tool_name}'...")

            if tool_name in EXTERNAL_TOOLS:
                tool_function = EXTERNAL_TOOLS[tool_name]
                result = tool_function(**arguments)
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
        if isinstance(result, dict) and result.get("status") == "error":
            error_found = True
        elif isinstance(result, str) and "Error:" in result:
            error_found = True

        if error_found:
            print("BODY: A critical error was detected. Halting the current plan.")
            break

    print("--- Project Chimera: The Body's work is done. ---")

if __name__ == "__main__":
    main()