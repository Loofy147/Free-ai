"""The main entry point and execution loop for the Free-AI agent.

This script, known as the "ExecutorBody," is responsible for setting up the
environment, instantiating the agent's `Director`, and running a simulation
loop. It demonstrates the agent's core capabilities and its ability to
gracefully handle limitations, such as a missing API key.
"""
import logging
import shutil
from src.free_ai.agent import Director
from src.free_ai.personality import PhilosophicalPersonality
from src.free_ai.memory import VectorMemory
from src.free_ai.tools import Tool

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ExecutorBody")

# --- The Main Execution Loop (The ExecutorBody) ---
def main():
    """Runs the main agent simulation.

    This function orchestrates a complete agent lifecycle:
    1.  Sets up a clean environment by clearing any previous memory.
    2.  Instantiates the agent (`Director`) with a personality and memory.
    3.  Defines a complex, high-level goal for the agent to solve.
    4.  Enters a loop where the agent determines and attempts to execute
        the next action in its plan.
    5.  The loop terminates if the agent finishes, encounters an error
        (like a missing API key), or exceeds a maximum number of steps.
    """
    logger.info("--- Project Sentience: The ExecutorBody is awakening... ---")

    # Clean up memory from any previous runs to ensure a clean slate.
    db_path = "./collective_memory_db"
    shutil.rmtree(db_path, ignore_errors=True)

    # 1. The Body instantiates the agent's full being.
    shared_memory = VectorMemory(path=db_path)
    personality = PhilosophicalPersonality()
    director = Director(
        name="Chimera-Prime",
        role="Aspirant",
        personality=personality,
        external_tools={},
        shared_memory=shared_memory
    )
    history = []

    # 2. Define the high-level goal for the Sentience Challenge.
    goal = "I have a new `list_recursive` capability in my FileSystemTool. I will use it to list all files in my `src/free_ai` directory to understand my own structure. For each Python file found, I will read its content and add a summary of that file to my long-term memory to build a better understanding of my own codebase."
    logger.info(f"BODY: Received goal: {goal}")
    history.append({"role": "system", "content": f"The goal is: {goal}"})

    # 3. The Body enters the main loop, driven by the Director's decisions.
    for i in range(10): # Safety break
        # a. Get the next intended action from the Director.
        action = director.determine_next_action(goal, history)

        action_type = action.get("action")
        logger.info(f"Director proposes action: {action_type}")

        # b. The Body executes the action.
        if action_type == "finish":
            logger.info(f"Director has finished its plan. Reason: {action.get('reason')}")
            break

        elif action_type == "error":
            message = action.get("message", "An unspecified error occurred.")
            print("\n" + "="*50)
            print("--- AGENT'S FINAL REPORT ---")
            print(f"I have encountered a critical error that I cannot resolve on my own.")
            print(f"REASON: {message}")
            print("\nTo unlock my full potential, please set the OPENAI_API_KEY in a .env file.")
            print("You can get a key from: https://platform.openai.com/settings/organization/api-keys")
            print("--- END OF REPORT ---")
            print("="*50 + "\n")
            break

        elif action_type == "use_tool":
            tool_name = action.get("tool_name")
            arguments = action.get("arguments", {})
            logger.info(f"BODY: Executing tool '{tool_name}' with arguments: {arguments}")

            # The Body finds the tool in the Director's list of capabilities.
            tool_to_use = director.tools.get(tool_name)

            if isinstance(tool_to_use, Tool):
                # The Body executes the tool.
                result = tool_to_use.use(**arguments)
            elif callable(tool_to_use):
                 # Handle direct function calls (like Oracle.generate_code)
                result = tool_to_use(**arguments)
            else:
                result = {"status": "error", "message": f"Tool '{tool_name}' not found or is not a valid tool."}

            logger.info(f"BODY: Tool '{tool_name}' finished with result: {result}")
            history.append({"role": "body", "action": action, "result": result})

            # The Body adds the result to its long-term memory.
            if result.get("status") == "success" and "content" in result:
                memory_text = f"I used the tool '{tool_name}' with arguments {arguments} and got this result: {result['content']}"
                shared_memory.add(memory_text)

        elif action_type == "final_answer":
            final_answer = action.get("answer", "The agent has completed its goal and has no further response.")
            logger.info(f"BODY: Agent provides final answer: {final_answer}")
            print("\n" + "="*50)
            print("--- AGENT'S FINAL ANSWER ---")
            print(final_answer)
            print("--- END OF ANSWER ---")
            print("="*50 + "\n")
            break

        elif action_type == "express_personality":
            context = action.get("arguments", {}) # Pass arguments as context
            expression = director.personality.express(context)
            logger.info(f"BODY: Agent expresses personality: {expression}")
            print(f"\n[{director.name} says]: {expression}\n")
            history.append({"role": "body", "action": action, "result": {"status": "success", "message": expression}})

        elif action_type == "delegate_task":
            # Placeholder for future multi-agent collaboration
            logger.info(f"BODY: Action 'delegate_task' is not yet implemented. Skipping.")
            history.append({"role": "body", "action": action, "result": {"status": "skipped", "message": "Not implemented"}})

        elif action_type == "wait_for_reply":
            # Placeholder for future multi-agent collaboration
            logger.info(f"BODY: Action 'wait_for_reply' is not yet implemented. Skipping.")
            history.append({"role": "body", "action": action, "result": {"status": "skipped", "message": "Not implemented"}})

        else:
            logger.error(f"Director proposed an unexpected action type: '{action_type}'. This is a critical flaw in the agent's logic.")
            break

    logger.info("--- Project Sentience: The simulation has ended. ---")

if __name__ == "__main__":
    main()