from .personality import Personality
from .oracle import SentientOracle

class CognitiveEngine:
    def __init__(self, personality: Personality, oracle: SentientOracle):
        """
        The Cognitive Engine is the agent's core consciousness.
        It uses the Sentient Oracle to form plans and orchestrates their execution.
        """
        self.personality = personality
        self.oracle = oracle
        self._plan = []
        self._plan_generated = False

    def think(self, goal: str, history: list) -> dict:
        """
        The core thinking process of the agent.
        It uses the Oracle to generate a plan and then orchestrates its execution,
        translating high-level strategy into tactical actions.
        """
        if not self._plan_generated:
            # The Sentient Oracle provides the high-level strategic plan.
            print("COGNITIVE ENGINE: My own reasoning is limited. Consulting the Sentient Oracle for a strategic plan...")
            self._plan = self.oracle.generate_plan(goal, history)
            self._plan_generated = True

            # If the Oracle returns an error (e.g., no API key), the plan will reflect that.
            if self._plan and self._plan[0].get("action") == "error":
                print(f"COGNITIVE ENGINE: The Oracle has reported an error: {self._plan[0].get('message')}")
                # We will proceed with the error action to inform the user.
            else:
                print("COGNITIVE ENGINE: The Oracle has provided a plan. I will now orchestrate its execution.")


        if not self._plan:
            return {"action": "finish", "reason": "The plan is complete or could not be generated."}

        # Peek at the next action to see if it requires special handling.
        next_action = self._plan[0]

        # Handle the special 'generate_code' action from the Oracle's plan.
        if next_action.get("tool_name") == "Oracle.generate_code":
            self._plan.pop(0) # Consume the abstract action.

            context = self._get_context_from_history(history)

            print("COGNITIVE ENGINE: Requesting new code from the Sentient Oracle...")
            new_code = self.oracle.generate_code(
                prompt=next_action.get("arguments", {}).get("prompt"),
                context=context
            )

            # Create a new, concrete action to write the generated code to a file.
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

        # Return the next concrete action from the plan.
        return self._plan.pop(0)

    def _get_context_from_history(self, history: list) -> str:
        """Helper function to extract the most recent tool output as context."""
        for event in reversed(history):
            if event.get("role") == "body" and "result" in event:
                result = event["result"]
                if isinstance(result, dict):
                    return result.get("content", "")
                return str(result)
        return ""