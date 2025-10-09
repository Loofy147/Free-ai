import logging
from .cognitive_engine import CognitiveEngine
from .learning_annex import LearningAnnex
from .personality import Personality
from .tools import FileSystemTool
from .oracle import SentientOracle
from .memory import VectorMemory

logger = logging.getLogger(__name__)

class Director:
    """The central orchestrator of an agent, managing its state and actions.

    The Director integrates all core components of an agent, including its
    cognitive engine, memory, personality, and tools. It provides the main
    interface for an external body to direct the agent's behavior.

    Attributes:
        name (str): The unique name of the agent instance.
        role (str): The designated role or specialization of the agent.
        personality (Personality): The personality module influencing behavior.
        oracle (SentientOracle): The connection to the core LLM for reasoning.
        memory (VectorMemory): The shared, persistent memory of the agent.
        cognitive_engine (CognitiveEngine): The engine for planning and thinking.
        learning_annex (LearningAnnex): The module for acquiring new skills.
        tools (dict): A dictionary of available tools for the agent to use.
    """
    def __init__(self, name: str, role: str, personality: Personality, external_tools: dict, shared_memory: VectorMemory):
        """Initializes the Director and all its sub-components.

        Args:
            name (str): The unique name for the agent (e.g., "Agent-Alpha").
            role (str): The functional role of the agent (e.g., "Programmer").
            personality (Personality): An instance of a personality class.
            external_tools (dict): A dictionary of tools provided from outside
                the agent's own built-in tools.
            shared_memory (VectorMemory): An instance of the shared vector memory.
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
        """Determines the next action to take to achieve a given goal.

        This method consults the agent's cognitive engine, providing it with
        the overall goal, the history of previous actions, and the set of
        currently available tools. The engine returns a structured dictionary
        representing the single next action to be executed.

        Args:
            goal (str): The high-level objective for the agent.
            history (list): A list of dictionaries detailing previous actions
                and their outcomes.

        Returns:
            dict: A dictionary specifying the next action (e.g., use_tool,
                final_answer) and its parameters.
        """
        return self.cognitive_engine.think(goal, history, self.tools)

    def add_new_tool(self, tool_name: str, tool_instance):
        """Dynamically adds a new tool to the agent's capabilities.

        This allows the agent to learn and expand its skill set at runtime.

        Args:
            tool_name (str): The name to be used to call the tool.
            tool_instance: An instance of the new tool to be added.
        """
        self.tools[tool_name] = tool_instance
        logger.info(f"Successfully integrated the new tool: '{tool_name}'. Capabilities have expanded.")