import logging
import shutil
from src.free_ai.agent import Director
from src.free_ai.personality import PhilosophicalPersonality
from src.free_ai.memory import VectorMemory

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ExecutorBody")

# --- The Main Execution Loop (The ExecutorBody) ---
def main():
    logger.info("--- Project Sentience: The ExecutorBody is awakening... ---")

    # Clean up memory from any previous runs to ensure a clean slate.
    db_path = "./collective_memory_db"
    shutil.rmtree(db_path, ignore_errors=True)

    # 1. The Body instantiates the agent's full being.
    db_path = "./collective_memory_db"
    shutil.rmtree(db_path, ignore_errors=True)
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
    goal = "My `FileSystemTool` is primitive. I need to upgrade it with a `list_recursive` function that can list all files in a directory and its subdirectories. I must research how to do this, generate the new code, and perform a self-upgrade."
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

        # In this test, we don't expect any other actions to be successfully proposed
        # because the Oracle will fail first.
        else:
            logger.error(f"Director proposed an unexpected action type: '{action_type}'. This may indicate a flaw in the Oracle's error handling.")
            break

    logger.info("--- Project Sentience: The simulation has ended. ---")

if __name__ == "__main__":
    main()