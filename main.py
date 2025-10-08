import json
import logging
from src.free_ai.agent import Director
from src.free_ai.personality import WhimsicalPersonality
from src.free_ai.tools import FileSystemTool

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ExecutorBody")

# --- The Main Execution Loop (The ExecutorBody) ---

def main():
    logger.info("--- Project Carapace: The ExecutorBody is awakening... ---")

    # 1. The Body instantiates the Director with a chosen personality.
    personality = WhimsicalPersonality()
    director = Director(personality)
    history = []

    # 2. Define the high-level goal for the Carapace Challenge.
    goal = "Refactor your `FileSystemTool` to add a new `modify_file` operation that appends text to a file."
    logger.info(f"Received goal: {goal}")
    history.append({"role": "system", "content": f"The goal is: {goal}"})

    # 3. The Body enters the main loop, driven by the Director's decisions.
    for i in range(10): # Add a safety break to prevent infinite loops.
        # a. Get the next intended action from the Director.
        action = director.determine_next_action(goal, history)

        action_type = action.get("action")
        logger.info(f"Director proposes action: {action_type}")

        if action_type == "finish":
            logger.info(f"The Director has finished its plan. Reason: {action.get('reason')}")
            break

        # b. The Body executes the action.
        result = None
        if action_type == "express_personality":
            context = action.get("arguments", {}).get("context", "")
            result = personality.express(context=context)
            logger.info(f"Expressing personality: {result}")
            history.append({"role": "assistant", "content": result})

        elif action_type == "use_tool":
            tool_name = action.get("tool_name")
            arguments = action.get("arguments", {})

            logger.info(f"Preparing to use tool '{tool_name}'...")
            try:
                if tool_name in director.tools:
                    tool = director.tools[tool_name]
                    if hasattr(tool, 'use'):
                        result = tool.use(**arguments)
                    else:
                        result = tool(**arguments)
                else:
                    result = {"status": "error", "message": f"Tool '{tool_name}' not found."}
            except Exception as e:
                logger.error(f"An unexpected error occurred during the execution of tool '{tool_name}'.", exc_info=True)
                result = {"status": "error", "message": f"Unexpected runtime error: {type(e).__name__}: {e}"}


            logger.info(f"Tool '{tool_name}' executed. Result: {result}")
            history.append({"role": "body", "action_taken": action, "result": result})

        else:
            logger.error(f"The Director proposed an unknown action type: '{action_type}'")
            break

        # c. The Body checks for failure before continuing.
        error_found = False
        if isinstance(result, dict) and result.get("status") == "error":
            error_found = True

        if error_found:
            logger.error(f"A critical error was detected. Halting the plan. Reason: {result.get('message')}")
            break

    logger.info("--- Project Carapace: The Body's work is done. ---")

if __name__ == "__main__":
    main()