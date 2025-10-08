import logging
import time
import shutil
from src.free_ai.agent import Director
from src.free_ai.personality import WhimsicalPersonality, PhilosophicalPersonality
from src.free_ai.memory import VectorMemory

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ExecutorBody")

# --- The Body's External Tools ---
def google_search(query: str) -> dict:
    """A placeholder for the real google_search tool."""
    logger.info(f"Simulating Google Search for: '{query}'")
    if "liskov substitution" in query.lower():
        content = "The Liskov Substitution Principle states that objects of a superclass shall be replaceable with objects of a subclass without affecting the correctness of the program. It is the 'L' in the SOLID acronym."
        return {"status": "success", "content": content}
    return {"status": "success", "content": "No relevant results found."}

def final_answer(answer: str) -> dict:
    """A tool to provide the final answer and terminate the process."""
    logger.info(f"FINAL ANSWER: {answer}")
    return {"status": "success", "message": f"Final Answer: {answer}"}

EXTERNAL_TOOLS = {
    "google_search": google_search,
    "final_answer": final_answer,
}

# --- The Main Execution Loop (The ExecutorBody) ---
def run_agent_session(agent: Director, goal: str):
    """Runs a single goal-oriented session for a given agent."""
    logger.info(f"--- NEW SESSION for {agent.name} ({agent.role}) ---")
    logger.info(f"--- GOAL: {goal} ---")
    history = [{"role": "system", "content": f"The goal is: {goal}"}]
    agent.cognitive_engine._plan_generated = False # Reset plan for new goal

    for i in range(10): # Safety break
        action = agent.determine_next_action(goal, history)
        action_type = action.get("action")
        logger.info(f"'{agent.name}' proposes action: {action_type}")

        if action_type == "finish":
            logger.info("Director has finished its plan.")
            break

        result = None
        if action_type == "use_tool":
            tool_name = action.get("tool_name")
            arguments = action.get("arguments", {})
            logger.info(f"Preparing to use tool '{tool_name}'...")

            tool = EXTERNAL_TOOLS.get(tool_name) or agent.tools.get(tool_name)
            if tool:
                 result = tool.use(**arguments) if hasattr(tool, 'use') else tool(**arguments)
            else:
                result = {"status": "error", "message": f"Tool '{tool_name}' not found."}

            logger.info(f"Tool '{tool_name}' executed. Result: {result}")
            history.append({"role": "body", "action_taken": action, "result": result})

        # c. Update memory and check for failure.
        if isinstance(result, dict) and result.get("status") == "success":
            if action_type == "use_tool" and tool_name == "google_search":
                knowledge = f"Goal: {goal}\nAction: {action_type} on {tool_name}\nResult: {result.get('content')}"
                agent.memory.add(knowledge, metadata={"source_agent": agent.name})

        if isinstance(result, dict) and result.get("status") == "error":
            logger.error(f"A critical error was detected. Halting plan. Reason: {result.get('message')}")
            break

        # The loop should only terminate if the final_answer tool was just used.
        if action_type == "use_tool" and tool_name == "final_answer":
            break

def main():
    logger.info("--- Project Mnemosyne: The ExecutorBody is awakening... ---")

    # 1. Create the single, shared memory for the entire society.
    # Clean up from previous runs to ensure a fair test.
    db_path = "./collective_memory_db"
    shutil.rmtree(db_path, ignore_errors=True)
    shared_memory = VectorMemory(path=db_path)

    # --- SESSION 1: The Researcher's Task ---
    researcher_personality = PhilosophicalPersonality()
    researcher = Director(
        name="Researcher-Delta",
        role="Researcher",
        personality=researcher_personality,
        external_tools=EXTERNAL_TOOLS,
        shared_memory=shared_memory
    )
    goal_1 = "My goal is to research and understand the Liskov Substitution Principle."
    run_agent_session(researcher, goal_1)

    logger.info("\n\n--- SESSION BREAK: The Researcher's work is done and its memory is now part of the collective. A new agent will now be born. ---\n\n")

    # --- SESSION 2: The Manager's Task ---
    manager_personality = WhimsicalPersonality()
    manager = Director(
        name="Manager-Epsilon",
        role="Manager",
        personality=manager_personality,
        external_tools=EXTERNAL_TOOLS,
        shared_memory=shared_memory # Connects to the SAME memory.
    )
    goal_2 = "I need to explain the 'L' in SOLID to my team. What does it stand for?"
    run_agent_session(manager, goal_2)

    logger.info("--- Project Mnemosyne: The simulation has ended. ---")

if __name__ == "__main__":
    main()