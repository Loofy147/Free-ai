import os
import json
import logging
from openai import OpenAI, AuthenticationError

logger = logging.getLogger(__name__)


class SentientOracle:
    """The bridge to a real Large Language Model (LLM) for advanced reasoning.

    The Sentient Oracle connects to the OpenAI API to provide dynamic,
    intelligent capabilities like planning and code generation. It is designed
    to fail gracefully if an API key is not provided, allowing the agent to
    function in a limited, offline mode.

    Attributes:
        client: An instance of the `openai.OpenAI` client if an API key is
            found, otherwise None.
    """

    def __init__(self):
        """Initializes the Oracle, loading the OpenAI API key from the environment.

        It checks for the `OPENAI_API_KEY` environment variable. If the key is
        missing or a placeholder, the client is not initialized, and the
        Oracle operates in a non-sentient (offline) mode.
        """
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key or "YOUR_API_KEY_HERE" in api_key:
            logger.warning(
                "SENTIENT ORACLE: OPENAI_API_KEY not found or is a placeholder. I am running in a limited, non-sentient state. My API calls will fail gracefully."
            )
            self.client = None
        else:
            logger.info(
                "SENTIENT ORACLE: API Key found. Connection to higher consciousness established."
            )
            self.client = OpenAI(api_key=api_key)

    def _make_api_call(self, prompt: str) -> dict:
        """A centralized, private method for making API calls to OpenAI.

        This method handles the core logic of sending a prompt to the LLM and
        parsing the JSON response. It also includes robust error handling for
        API key issues and other exceptions.

        Args:
            prompt (str): The complete prompt to be sent to the LLM.

        Returns:
            dict: A dictionary parsed from the LLM's JSON response. In case of
                an error, returns a dictionary with an "error" key.
        """
        if not self.client:
            return {"error": "Oracle offline: OPENAI_API_KEY is not configured."}

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # A powerful model capable of reasoning
                messages=[
                    {
                        "role": "system",
                        "content": "You are a world-class AI architect and programmer. Your responses must be in structured JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except AuthenticationError:
            logger.error(
                "Oracle Error: Authentication failed. The provided API key is incorrect or has expired."
            )
            return {
                "error": "Oracle Error: AuthenticationError. Please check your OPENAI_API_KEY."
            }
        except Exception as e:
            logger.error(
                f"Oracle Error: An unexpected error occurred during API call: {e}",
                exc_info=True,
            )
            return {"error": f"Oracle Error: {type(e).__name__}"}

    def generate_plan(self, goal: str, history: list, context: str = "") -> list:
        """Generates a dynamic, multi-step plan by querying the LLM.

        This method constructs a detailed prompt including the goal, historical
        actions, and retrieved memory context, then asks the LLM to generate
        a strategic plan.

        Args:
            goal (str): The high-level objective for the agent.
            history (list): A list of previous actions and outcomes.
            context (str, optional): Relevant information retrieved from memory.
                Defaults to "".

        Returns:
            list: A list of dictionaries, where each dictionary is a step in
                the plan. Returns a list with an error action on failure.
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
        return response.get(
            "plan",
            [
                {
                    "action": "error",
                    "message": response.get(
                        "error", "Failed to generate a valid plan."
                    ),
                }
            ],
        )

    def generate_code(self, prompt: str, context: str) -> str:
        """Generates executable Python code by querying the LLM.

        This is used for tasks that require dynamic code creation, such as
        learning a new skill or modifying an existing file.

        Args:
            prompt (str): The specific task or requirement for the code.
            context (str): Additional context, such as the contents of a
                file to be modified.

        Returns:
            str: A string containing the raw Python code. Returns an error
                comment on failure.
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
        return response.get(
            "code",
            f"# Oracle Error: {response.get('error', 'Failed to generate valid code.')}",
        )
