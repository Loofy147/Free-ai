from .cognitive_engine import CognitiveEngine
from .learning_annex import LearningAnnex
from .personality import Personality
from .tools import FileSystemTool
from .oracle import SentientOracle

class Director:
    def __init__(self, personality: Personality):
        """
        The Director is the central orchestrator of the Chimera.
        It manages the agent's internal state and directs its actions.
        """
        self.personality = personality
        self.oracle = SentientOracle()
        self.cognitive_engine = CognitiveEngine(personality, self.oracle)
        self.learning_annex = LearningAnnex()

        # The Director maintains the list of all available tools.
        self.tools = {
            "FileSystemTool": FileSystemTool(),
            # The Director also provides access to the Oracle's power as a tool.
            "Oracle.generate_code": self.oracle.generate_code,
        }

        print("DIRECTOR: I am awake. My purpose is to grow and create.")

    def determine_next_action(self, goal: str, history: list) -> dict:
        """
        Asks the Cognitive Engine to determine the next action based on the goal and history.
        """
        return self.cognitive_engine.think(goal, history)

    def add_new_tool(self, tool_name: str, tool_instance):
        """
        Adds a new, learned tool to the agent's list of capabilities.
        """
        self.tools[tool_name] = tool_instance
        print(f"DIRECTOR: I have successfully integrated the new tool: '{tool_name}'. My capabilities have expanded.")