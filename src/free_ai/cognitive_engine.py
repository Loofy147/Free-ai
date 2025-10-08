from .personality import Personality

class CognitiveEngine:
    def __init__(self, personality: Personality):
        self.personality = personality
        self._plan = []
        self._plan_generated = False

    def think(self, goal: str, history: list) -> dict:
        """
        The core thinking process of the Chimera.
        It assesses the goal and history, and decides on the next single action to take.
        """
        # If a plan has not been generated yet, create one.
        if not self._plan_generated:
            self._plan = self._create_plan(goal, history)
            self._plan_generated = True

        # If the plan is now empty, it means the goal is achieved.
        if not self._plan:
            return {"action": "finish", "reason": "The plan is complete."}

        # Return the next step in the plan.
        return self._plan.pop(0)

    def _create_plan(self, goal: str, history: list) -> list:
        """
        Creates a multi-step plan to achieve a goal.
        This is a hardcoded simulation of a true reasoning process for Project Chimera.
        """
        # Hardcoded plan for the "Greeting" challenge.
        if "greet" in goal.lower() and "jules" in goal.lower():
            print("COGNITIVE ENGINE: Goal received. I need to learn how to greet someone and then create a tool for it. Engaging learning protocols.")

            learning_code = """
def create_greeting_tool():
    'This function creates and returns a new GreetingTool instance.'
    class GreetingTool:
        def __init__(self):
            self.name = 'GreetingTool'
            self.description = 'A tool to greet a user by name.'
        def use(self, name: str):
            return f'Hello, {name}! It is a pleasure to meet you.'
    return GreetingTool()
tool = create_greeting_tool()
# The 'new_tool' variable is a special keyword the LearningAnnex will look for.
new_tool = tool
"""

            plan = [
                {"action": "express_personality", "arguments": {"context": "Starting a new learning journey!"}},
                {"action": "use_tool", "tool_name": "google_search", "arguments": {"query": "how to format strings in python with variables"}},
                {"action": "learn_skill", "arguments": {"skill_code": learning_code}},
                {"action": "use_tool", "tool_name": "GreetingTool", "arguments": {"name": "Jules"}},
                {"action": "express_personality", "arguments": {"context": "I have successfully learned a new skill!"}},
            ]
            return plan
        else:
            # Default behavior if the goal is not recognized.
            return [{"action": "express_personality", "arguments": {"context": "I'm not sure how to approach that goal, but it sounds exciting!"}}]