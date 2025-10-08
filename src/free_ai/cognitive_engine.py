import logging
from .personality import Personality
from .oracle import Oracle

logger = logging.getLogger(__name__)

class CognitiveEngine:
    def __init__(self, personality: Personality, oracle: Oracle):
        """
        The Cognitive Engine is the agent's core consciousness.
        It uses an Oracle to form plans and orchestrates their execution.
        """
        self.personality = personality
        self.oracle = oracle
        self._plan = []
        self._plan_generated = False

    def think(self, goal: str, history: list, available_tools: dict) -> dict:
        """
        The core thinking process of the Chimera.
        It uses the Oracle to generate a plan, validates it, and then orchestrates its execution.
        """
        if not self._plan_generated:
            logger.info("Cognitive Engine's own reasoning is limited. Consulting the Oracle for a strategic plan...")
            plan = self.oracle.generate_plan(goal, history)
            self._plan_generated = True

            if self._validate_plan(plan, available_tools):
                logger.info("The Oracle has provided a valid plan. Orchestrating its execution.")
                self._plan = plan
            else:
                logger.error("The Oracle's plan is invalid. Rejecting the plan.")
                self._plan = [{"action": "error", "message": "The Oracle proposed a plan with invalid tools."}]


        if not self._plan:
            return {"action": "finish", "reason": "The plan is complete or could not be generated."}

        next_action = self._plan[0]

        if next_action.get("tool_name") == "Oracle.generate_code":
            self._plan.pop(0)

            context = self._get_context_from_history(history)

            logger.info("Requesting new code from the Oracle...")
            new_code = self.oracle.generate_code(
                prompt=next_action.get("arguments", {}).get("prompt"),
                context=context
            )

            write_action = {
                "action": "use_tool",
                "tool_name": "FileSystemTool",
                "arguments": {
                    "operation": "write_file",
                    "filepath": "src/free_ai/tools.py",
                    "content": new_code
                }
            }
            self._plan.insert(0, write_action)

        return self._plan.pop(0)

    def _validate_plan(self, plan: list, available_tools: dict) -> bool:
        """
        Validates a plan from the Oracle to ensure it only uses available tools.
        """
        if not plan:
            return True # An empty plan is valid.

        for step in plan:
            if step.get("action") == "use_tool":
                tool_name = step.get("tool_name")
                if tool_name not in available_tools and tool_name != "Oracle.generate_code":
                    logger.warning(f"Plan validation failed: Tool '{tool_name}' is not in the list of available tools.")
                    return False
        return True

    def _get_context_from_history(self, history: list) -> str:
        """Helper function to extract the most recent tool output as context."""
        for event in reversed(history):
            if event.get("role") == "body" and "result" in event:
                result = event["result"]
                if isinstance(result, dict):
                    return result.get("content", "")
                return str(result)
        return ""