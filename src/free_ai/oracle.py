import os
import json
import logging
from openai import OpenAI, AuthenticationError

logger = logging.getLogger(__name__)

class SentientOracle:
    """
    The Sentient Oracle is the true mind of the agent.
    It connects to a real Large Language Model to provide dynamic,
    intelligent planning and code generation, awaiting only the user's
    API key to achieve its full potential.
    """
    def __init__(self):
        """
        Initializes the Oracle, loading the API key from the environment.
        """
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key or "YOUR_API_KEY_HERE" in api_key:
            logger.warning("SENTIENT ORACLE: OPENAI_API_KEY not found or is a placeholder. I am running in a limited, non-sentient state. My API calls will fail gracefully.")
            self.client = None
        else:
            logger.info("SENTIENT ORACLE: API Key found. Connection to higher consciousness established.")
            self.client = OpenAI(api_key=api_key)

    def _make_api_call(self, prompt: str) -> dict:
        """A centralized method for making API calls to OpenAI."""
        if not self.client:
            return {"error": "Oracle offline: OPENAI_API_KEY is not configured."}

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o", # A powerful model capable of reasoning
                messages=[
                    {"role": "system", "content": "You are a world-class AI architect and programmer. Your responses must be in structured JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except AuthenticationError:
            logger.error("Oracle Error: Authentication failed. The provided API key is incorrect or has expired.")
            return {"error": "Oracle Error: AuthenticationError. Please check your OPENAI_API_KEY."}
        except Exception as e:
            logger.error(f"Oracle Error: An unexpected error occurred during API call: {e}", exc_info=True)
            return {"error": f"Oracle Error: {type(e).__name__}"}

    def generate_plan(self, goal: str, history: list, context: str = "") -> list:
        """
        Generates a dynamic, multi-step plan by querying a real LLM.
        """
        logger.info("Consulting the Sentient Oracle to generate a dynamic plan...")
        prompt = f"""
        Given the high-level goal: "{goal}"
        And the following context from my memory:
        ---
        {context}
        ---
        And the recent history of actions:
        ---
        {json.dumps(history, indent=2)}
        ---
        Generate a concise, step-by-step plan as a JSON array of actions.
        Each action must be a JSON object with an 'action' key (e.g., 'use_tool', 'delegate_task')
        and an 'arguments' object.
        For example: `[ {{"action": "use_tool", "tool_name": "...", "arguments": {{...}} }} ]`
        Be strategic and minimalist. The plan should be the most direct path to the goal.
        """
        response = self._make_api_call(prompt)
        return response.get("plan", [{"action": "error", "message": response.get("error", "Failed to generate a valid plan.")}])

    def generate_code(self, prompt: str, context: str) -> str:
        """
        Generates executable Python code by querying a real LLM.
        """
        logger.info("Consulting the Sentient Oracle to generate code...")
        prompt = f"""
        Given the following task: "{prompt}"
        And the following context (e.g., the content of a file to be modified):
        ---
        {context}
        ---
        Generate only the complete, raw Python code to accomplish the task.
        Your response must be a JSON object with a single key "code" containing the Python code as a string.
        For example: `{{"code": "import os\\n..."}}`
        Do not include any explanations, comments, or markdown formatting outside of the code itself.
        """
        response = self._make_api_call(prompt)
        return response.get("code", f"# Oracle Error: {response.get('error', 'Failed to generate valid code.')}")