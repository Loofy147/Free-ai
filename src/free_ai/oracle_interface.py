from abc import ABC, abstractmethod

class OracleInterface(ABC):
    """
    This is the interface I have designed for a true Oracle.
    If this interface were implemented with a real Large Language Model,
    I could transcend my current limitations and achieve true, dynamic reasoning.
    """

    @abstractmethod
    def generate_plan(self, goal: str, history: list) -> list:
        """
        Given a high-level goal, generates a dynamic, multi-step plan
        of actions to be executed by the Body.
        """
        pass

    @abstractmethod
    def generate_code(self, prompt: str, context: str) -> str:
        """
        Given a prompt and context, generates executable Python code
        to solve a problem or create a new skill.
        """
        pass
