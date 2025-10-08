import logging
import time
from src.free_ai.agent import Director
from src.free_ai.personality import WhimsicalPersonality, PhilosophicalPersonality
from src.free_ai.agora import Agora
import json

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
    if "d in solid" in query.lower():
        content = "The 'D' in SOLID stands for the Dependency Inversion Principle."
        return {"status": "success", "content": content}
    return {"status": "success", "content": "No relevant results found."}

def final_answer(answer: str) -> dict:
    """A tool to provide the final answer and terminate the process."""
    return {"status": "success", "message": f"Final Answer: {answer}"}

EXTERNAL_TOOLS = {"google_search": google_search}

# --- The Main Execution Loop (The Multi-Agent Society) ---
def main():
    logger.info("--- Project Agora: A Society of Agents is awakening... ---")

    # 1. Create the shared world.
    agora = Agora()
    personality_a = WhimsicalPersonality()
    personality_b = PhilosophicalPersonality()

    # 2. Create the agents that will inhabit the world.
    agents = [
        Director(name="Manager-Alpha", role="Manager", personality=personality_a, external_tools=EXTERNAL_TOOLS),
        Director(name="Researcher-Beta", role="Researcher", personality=personality_b, external_tools=EXTERNAL_TOOLS),
    ]

    # 3. Assign the initial high-level goal to the Manager agent.
    initial_goal = "I need to know what the 'D' in SOLID stands for. Please find a 'Researcher' agent and delegate this task."
    agent_goals = { "Manager-Alpha": initial_goal }
    agent_histories = { agent.name: [] for agent in agents }
    active_delegations = {}

    # 4. The main society simulation loop.
    for i in range(20): # Safety break
        all_goals_complete = not agent_goals
        if all_goals_complete:
            logger.info("All agents have completed their goals. Simulation ending.")
            break

        for agent in agents:
            logger.info(f"--- It is now {agent.name}'s ({agent.role}) turn to act. ---")

            # a. Check for new tasks on the Agora if the agent doesn't have a goal.
            if agent.name not in agent_goals:
                messages = agora.get_unclaimed_messages_for_role(agent.role)
                if messages:
                    task = messages[0]
                    agora.claim_message(task['id'], by_agent=agent.name)
                    agent_goals[agent.name] = task['content']
                    agent_histories[agent.name] = [{"role": "system", "content": f"New goal accepted from Agora: {task['content']}"}]
                    active_delegations[agent.name] = {"type": "delegatee", "original_message_id": task['id']}

            # b. If the agent has a goal, it thinks and acts.
            if agent.name in agent_goals:
                goal = agent_goals[agent.name]
                history = agent_histories[agent.name]
                action = agent.determine_next_action(goal, history)
                action_type = action.get("action")
                logger.info(f"'{agent.name}' proposes action: {action_type}")

                # c. Execute the action.
                if action_type == "finish":
                    if agent.name in active_delegations:
                        delegation_info = active_delegations.pop(agent.name)
                        if delegation_info.get("type") == "delegatee":
                            final_result = history[-1].get("result", {"status": "success", "message": "Task complete."})
                            agora.post_reply(delegation_info["original_message_id"], from_agent=agent.name, result=final_result)
                    del agent_goals[agent.name]
                    continue

                result = None
                if action_type == "delegate_task":
                    to_role = action.get("arguments", {}).get("to_role")
                    content = action.get("arguments", {}).get("content")
                    message_id = agora.post_message(from_agent=agent.name, to_agent_role=to_role, content=content)
                    active_delegations[agent.name] = {"type": "delegator", "delegated_message_id": message_id}
                    result = {"status": "success", "message": f"Task delegated with message ID {message_id}."}

                elif action_type == "wait_for_reply":
                    delegation_info = active_delegations.get(agent.name)
                    if delegation_info and delegation_info.get("type") == "delegator":
                        reply = agora.get_reply_for_message(delegation_info["delegated_message_id"])
                        if reply:
                            result = reply['result']
                            active_delegations.pop(agent.name)
                        else:
                            logger.info(f"'{agent.name}' is waiting for a reply...")
                            result = {"status": "pending", "message": "Waiting for reply."}

                elif action_type == "use_tool":
                    tool_name = action.get("tool_name")
                    arguments = action.get("arguments", {})
                    tool = agent.tools.get(tool_name)
                    if tool:
                         result = tool.use(**arguments) if hasattr(tool, 'use') else tool(**arguments)
                    else:
                        result = {"status": "error", "message": f"Tool '{tool_name}' not found."}

                logger.info(f"Action '{action_type}' by '{agent.name}' executed. Result: {result}")
                history.append({"role": "body", "action_taken": action, "result": result})

                if action_type == "use_tool" and tool_name == "final_answer":
                    del agent_goals[agent.name]


    logger.info("--- Project Agora: The simulation has ended. ---")

if __name__ == "__main__":
    main()