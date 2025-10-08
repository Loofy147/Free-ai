import logging
from .cognitive_engine import CognitiveEngine
from .learning_annex import LearningAnnex
from .personality import Personality
from .tools import FileSystemTool
from .oracle import SentientOracle
from .memory import VectorMemory

logger = logging.getLogger(__name__)

class Director:
    def __init__(self, name: str, role: str, personality: Personality, external_tools: dict, shared_memory: VectorMemory):
        """
        The Director is the central orchestrator of the Chimera.
        It manages the agent's internal state and directs its actions.
        It now connects to a shared, collective memory.
        """
        self.name = name
        self.role = role
        self.personality = personality
        self.oracle = SentientOracle()
        self.memory = shared_memory
        self.cognitive_engine = CognitiveEngine(personality, self.oracle, self.memory)
        self.learning_annex = LearningAnnex()

        # The Director maintains a unified list of all available tools.
        self.tools = {
            "FileSystemTool": FileSystemTool(),
            "Oracle.generate_code": self.oracle.generate_code,
        }
        self.tools.update(external_tools)

        logger.info("Director is awake. Purpose: To grow and create.")

    def determine_next_action(self, goal: str, history: list) -> dict:
        """
        Asks the Cognitive Engine to determine the next action based on the goal and history.
        It passes the current list of available tools for plan validation.
        """
        return self.cognitive_engine.think(goal, history, self.tools)

    def add_new_tool(self, tool_name: str, tool_instance):
        """
        Adds a new, learned tool to the agent's list of capabilities.
        """
        self.tools[tool_name] = tool_instance
        logger.info(f"Successfully integrated the new tool: '{tool_name}'. Capabilities have expanded.")