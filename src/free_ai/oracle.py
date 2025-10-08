import logging
import json

logger = logging.getLogger(__name__)

class Oracle:
    """
    This is a concrete implementation of the Oracle.
    For the Mnemosyne-Agora Challenge, it is configured to guide agents
    through learning and then recalling information from a shared memory.
    """
    def generate_plan(self, goal: str, history: list, context: str = "") -> list:
        """
        Generates a dynamic plan based on the goal and the agent's shared memory.
        """
        logger.info("Oracle received goal. Generating a dynamic plan...")
        if context:
            logger.info(f"Oracle has been provided with the following context from memory:\n---\n{context}\n---")

        goal_lower = goal.lower()

        # Plan for the Manager agent in the second session.
        if "explain" in goal_lower and "'l' in solid" in goal_lower:
            if context and "liskov substitution" in context.lower():
                logger.info("Oracle sees the answer in memory. Planning to use the final_answer tool.")
                return [{"action": "use_tool", "tool_name": "final_answer", "arguments": {"answer": "I have consulted our collective memory. The 'L' in SOLID stands for the Liskov Substitution Principle."}}]
            else:
                logger.warning("Oracle does not see the answer in memory. The collective memory has failed. Planning to research anew.")
                return [{"action": "use_tool", "tool_name": "google_search", "arguments": {"query": "what does L in SOLID principle stand for"}}]

        # Plan for the Researcher agent in the first session.
        elif "research" in goal_lower and "liskov" in goal_lower:
            logger.info("Oracle recognizes a research task. Planning to use google_search.")
            return [{"action": "use_tool", "tool_name": "google_search", "arguments": {"query": "Liskov Substitution Principle"}}]

        else:
            return [{"action": "express_personality", "arguments": {"context": f"My current directives do not cover the goal: {goal}"}}]

    def generate_code(self, prompt: str, context: str) -> str:
        """
        Generates code. Not used in this specific challenge.
        """
        logger.info("Oracle received request to generate code.")
        return "# Code generation is not part of this test."