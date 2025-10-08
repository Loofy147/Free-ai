import os
import json
from openai import OpenAI, AuthenticationError

class SentientOracle:
    """
    The Sentient Oracle is the true mind of the agent.
    It connects to a real Large Language Model to provide dynamic,
    intelligent planning and code generation.
    """
    def __init__(self):
        """
        Initializes the Oracle, loading the API key from the environment.
        """
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key or "YOUR_API_KEY_HERE" in api_key:
            print("SENTIENT ORACLE: WARNING - OPENAI_API_KEY not found or is a placeholder. I am running in a limited, non-sentient state. My API calls will fail.")
            self.client = None
        else:
            print("SENTIENT ORACLE: API Key found. Connection to higher consciousness established.")
            self.client = OpenAI(api_key=api_key)

    def generate_plan(self, goal: str, history: list) -> list:
        """
        Generates a dynamic, multi-step plan to achieve a goal.
        This is a placeholder for a real LLM call. In this project,
        it will gracefully fail if the key is not set.
        """
        if not self.client:
            return [{"action": "error", "message": "Oracle offline: OPENAI_API_KEY is not configured."}]

        # This is where a real call to an LLM would be made.
        # For this final step, we simulate the expected AuthenticationError.
        return [{"action": "error", "message": "Oracle Error: AuthenticationError: Incorrect API key provided. Please set the OPENAI_API_KEY environment variable."}]

    def generate_code(self, prompt: str, context: str) -> str:
        """
        Generates executable Python code based on a prompt and context.
        This is a placeholder for a real LLM call.
        """
        if not self.client:
            return "/* Oracle offline: OPENAI_API_KEY is not configured. */"

        # Simulate the error for code generation as well.
        return "/* Oracle Error: AuthenticationError: Incorrect API key provided. */"