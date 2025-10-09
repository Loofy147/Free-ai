import logging
import json
from typing import Dict, List, Union
from .personality import Personality
from .oracle import SentientOracle
from .memory import VectorMemory

logger = logging.getLogger(__name__)

class CognitiveEngine:
    """The core consciousness of the agent, responsible for planning.

    The CognitiveEngine uses a Retrieval-Augmented Generation (RAG) process
    to formulate plans. It first queries the agent's `VectorMemory` for
    relevant context, then provides that context to the `SentientOracle` to
    generate a multi-step plan. It also validates the plan to ensure it is
    executable by the agent.

    Attributes:
        personality (Personality): The personality module for the agent.
        oracle (SentientOracle): The LLM interface for reasoning and planning.
        memory (VectorMemory): The agent's long-term semantic memory.
        _plan (list): The current multi-step plan being executed.
        _plan_generated (bool): A flag indicating if a plan has been generated.
    """
    def __init__(self, personality: Personality, oracle: SentientOracle, memory: VectorMemory):
        """Initializes the CognitiveEngine.

        Args:
            personality (Personality): An instance of a personality class.
            oracle (SentientOracle): An instance of the SentientOracle.
            memory (VectorMemory): An instance of the VectorMemory.
        """
        self.personality = personality
        self.oracle = oracle
        self.memory = memory
        self._plan = []
        self._plan_generated = False

    def think(self, goal: Union[str, Dict], history: list, available_tools: dict) -> dict:
        """Generates a plan and returns the next action.

        This is the main entry point for the agent's thinking process. If a
        plan has not yet been generated for the current goal, it uses RAG to
        create one. It then returns the next action from the plan.

        Args:
            goal (Union[str, Dict]): The high-level objective or task.
            history (list): A log of previous actions and outcomes.
            available_tools (dict): A dictionary of tools the agent can use.

        Returns:
            dict: A dictionary representing the next action to be executed.
        """
        if not self._plan_generated:
            logger.info("Cognitive Engine consulting memory and Oracle for a strategic plan...")

            # RAG Step 1: Retrieve context. The query can be the goal string or a task description.
            query_text = goal if isinstance(goal, str) else json.dumps(goal)
            logger.info(f"Querying memory for context related to: '{query_text[:100]}...'")
            retrieved_context = self.memory.query(query_text)
            context_str = "\n".join(retrieved_context)

            # RAG Step 2: Generate plan from Oracle.
            plan = self.oracle.generate_plan(goal, history, context_str)
            self._plan_generated = True

            if self._validate_plan(plan, available_tools):
                logger.info("The Oracle has provided a valid plan. Orchestrating its execution.")
                self._plan = plan
            else:
                logger.error("The Oracle's plan is invalid. Rejecting the plan.")
                self._plan = [{"action": "error", "message": "The Oracle proposed a plan with invalid tools."}]

        if not self._plan:
            return {"action": "finish", "reason": "The plan is complete or could not be generated."}

        return self._plan[0]

    def advance_plan(self):
        """Removes the current action from the plan, advancing to the next step."""
        if self._plan:
            self._plan.pop(0)
            logger.info("Cognitive Engine advanced to the next step in the plan.")

    def _validate_plan(self, plan: list, available_tools: dict) -> bool:
        """Validates an Oracle-generated plan against available tools and actions.

        This is a critical security and stability check to ensure the LLM has
        not hallucinated a non-existent tool or action.

        Args:
            plan (list): The list of action dictionaries from the Oracle.
            available_tools (dict): A dictionary of tools the agent can currently use.

        Returns:
            bool: True if the plan is valid, False otherwise.
        """
        if not plan:
            return True

        VALID_ACTIONS = ["use_tool", "express_personality", "delegate_task", "wait_for_reply", "final_answer", "error"]

        for step in plan:
            action_type = step.get("action")
            if action_type not in VALID_ACTIONS:
                logger.warning(f"Plan validation failed: Action type '{action_type}' is not recognized.")
                return False

            if action_type == "use_tool":
                tool_name = step.get("tool_name")
                if tool_name not in available_tools:
                    logger.warning(f"Plan validation failed: Tool '{tool_name}' is not in the list of available tools: {list(available_tools.keys())}")
                    return False
        return True

    def _get_context_from_history(self, history: list) -> str:
        """Helper function to extract the most recent tool output as context.

        Args:
            history (list): A list of event dictionaries from the main loop.

        Returns:
            str: The content of the most recent tool output, or an empty string.
        """
        for event in reversed(history):
            if event.get("role") == "body" and "result" in event:
                result = event["result"]
                if isinstance(result, dict):
                    return result.get("content", "")
                return str(result)
        return ""