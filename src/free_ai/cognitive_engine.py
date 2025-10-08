import logging
import json
from typing import Dict, List, Union
from .personality import Personality
from .oracle import SentientOracle
from .memory import VectorMemory

logger = logging.getLogger(__name__)

class CognitiveEngine:
    def __init__(self, personality: Personality, oracle: SentientOracle, memory: VectorMemory):
        """
        The Cognitive Engine is the agent's core consciousness.
        It uses an Oracle and its own VectorMemory to form plans and orchestrate their execution.
        """
        self.personality = personality
        self.oracle = oracle
        self.memory = memory
        self._plan = []
        self._plan_generated = False

    def think(self, goal: Union[str, Dict], history: list, available_tools: dict) -> dict:
        """
        The core thinking process of the Chimera.
        It uses Retrieval-Augmented Generation (RAG) to form a plan.
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

        return self._plan.pop(0)

    def _validate_plan(self, plan: list, available_tools: dict) -> bool:
        """
        Validates a plan from the Oracle to ensure it only uses available and valid actions.
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
        """Helper function to extract the most recent tool output as context."""
        for event in reversed(history):
            if event.get("role") == "body" and "result" in event:
                result = event["result"]
                if isinstance(result, dict):
                    return result.get("content", "")
                return str(result)
        return ""