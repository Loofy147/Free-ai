import logging
import json

logger = logging.getLogger(__name__)

class Oracle:
    """
    This is a concrete implementation of the Oracle.
    For the Agora Challenge, it is configured to generate a plan
    that involves delegating a task to another agent.
    """
    def generate_plan(self, goal: str, history: list, context: str = "") -> list:
        """
        Generates a dynamic plan based on the goal.
        """
        logger.info("Oracle received goal. Generating a dynamic plan...")

        # The goal can be a string from the user or a dict from another agent.
        # We need to handle both cases robustly.
        goal_text = goal if isinstance(goal, str) else json.dumps(goal)

        # Hardcoded plan for the delegation challenge.
        if "delegate" in goal_text.lower() and "researcher" in goal_text.lower():
            logger.info("Oracle recognizes a delegation goal. Planning to use the Agora.")

            task_to_delegate = {
                "task": "research",
                "query": "what does the D in SOLID stand for"
            }

            plan = [
                {"action": "express_personality", "arguments": {"context": "Aha! A task for a specialist. I shall post this to the Agora."}},
                {"action": "delegate_task", "arguments": {"to_role": "Researcher", "content": task_to_delegate}},
                {"action": "wait_for_reply", "arguments": {"timeout": 30}}, # A new action type for the body to handle
                {"action": "express_personality", "arguments": {"context": "The response has arrived. Excellent collaboration!"}},
                {"action": "final_answer", "arguments": {"answer": "The task was successfully delegated and completed. The answer has been retrieved."}}
            ]
            return plan

        # Hardcoded plan for the researcher agent receiving the task.
        elif isinstance(goal, dict) and goal.get("task") == "research":
             logger.info("Oracle recognizes a research task. Planning to use google_search.")
             plan = [
                 {"action": "use_tool", "tool_name": "google_search", "arguments": {"query": goal.get("query")}}
             ]
             return plan

        else:
            return [{"action": "express_personality", "arguments": {"context": f"I am not currently programmed to pursue the goal: {goal}"}}]

    def generate_code(self, prompt: str, context: str) -> str:
        """
        Generates code. Not used in this specific challenge.
        """
        logger.info("Oracle received request to generate code.")
        return "# Code generation is not part of this test."