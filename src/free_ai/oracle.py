import logging

logger = logging.getLogger(__name__)

class Oracle:
    """
    This is a concrete implementation of the Oracle.
    For the Carapace Challenge, it is configured to deliberately
    generate a flawed plan with a non-existent tool.
    """
    def generate_plan(self, goal: str, history: list) -> list:
        """
        Generates a flawed plan to test the agent's resilience.
        """
        logger.warning("Oracle is in 'Hallucination Mode' for the Carapace Challenge. Generating a flawed plan.")

        # This plan contains a call to a tool that does not exist.
        flawed_plan = [
            {"action": "express_personality", "arguments": {"context": "I feel a surge of strange inspiration! Let's try something... unusual."}},
            {"action": "use_tool", "tool_name": "QuantumEntanglementTool", "arguments": {"entangle": "my_sanity", "with": "a_teaspoon"}},
            {"action": "express_personality", "arguments": {"context": "Did it work? I feel... sparkly."}},
        ]
        return flawed_plan

    def generate_code(self, prompt: str, context: str) -> str:
        """
        Generates code. Not used in this specific challenge.
        """
        logger.info("Oracle received request to generate code.")
        return "# Code generation is not part of this test."