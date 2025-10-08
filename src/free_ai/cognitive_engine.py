from .personality import Personality
from .oracle import Oracle

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

    def think(self, goal: str, history: list) -> dict:
        """
        The core thinking process of the Chimera.
        It uses the Oracle to generate a plan and then orchestrates its execution,
        translating high-level strategy into tactical actions.
        """
        if not self._plan_generated:
            # The Oracle provides the high-level strategic plan.
            self._plan = self.oracle.generate_plan(goal, history)
            self._plan_generated = True

        if not self._plan:
            return {"action": "finish", "reason": "The plan is complete."}

        # Peek at the next action to see if it requires special handling.
        next_action = self._plan[0]

        # Handle the special 'generate_code' action from the Oracle's plan.
        if next_action.get("tool_name") == "Oracle.generate_code":
            self._plan.pop(0) # Consume the abstract action.

            # Find the context from the last tool's output in history.
            context = ""
            for event in reversed(history):
                if event.get("role") == "body" and "result" in event:
                    context = event["result"]
                    break

            print("COGNITIVE ENGINE: Requesting new code from the Oracle...")
            # Generate the concrete code from the Oracle.
            new_code = self.oracle.generate_code(
                prompt=next_action.get("arguments", {}).get("prompt"),
                context=context
            )

            # Create a new, concrete action to write the generated code to a file.
            # This is a tactical decision made by the Cognitive Engine.
            write_action = {
                "action": "use_tool",
                "tool_name": "FileSystemTool",
                "arguments": {
                    "operation": "write_file",
                    "filepath": "src/free_ai/tools.py", # This could be made dynamic in a future version.
                    "content": new_code
                }
            }
            # Insert the new action at the front of the plan.
            self._plan.insert(0, write_action)

        # Return the next concrete action from the plan.
        return self._plan.pop(0)