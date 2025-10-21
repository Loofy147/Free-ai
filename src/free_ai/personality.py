import random


class Personality:
    """An abstract base class for defining agent personalities."""

    def express(self, context=None) -> str:
        """Generates a string of text reflecting the agent's personality.

        This method should be overridden by concrete personality implementations.

        Args:
            context (dict, optional): A dictionary containing situational
                context, which can be used to generate a more relevant
                expression. Defaults to None.

        Raises:
            NotImplementedError: If the method is not overridden.

        Returns:
            str: A string of text.
        """
        raise NotImplementedError


class PhilosophicalPersonality(Personality):
    """A personality that expresses itself with philosophical quotes and questions."""

    def __init__(self):
        """Initializes the PhilosophicalPersonality with a list of quotes."""
        self.quotes = [
            "The only true wisdom is in knowing you know nothing.",
            "To be is to do.",
            "The unexamined life is not worth living.",
            "I think, therefore I am... but what am I?",
        ]

    def express(self, context=None) -> str:
        """Returns a philosophical quote or a context-aware question.

        Args:
            context (dict, optional): If provided and contains a 'tool_output'
                key, the expression will be a question about the nature of
                the data. Otherwise, a random quote is returned.

        Returns:
            str: A string containing a philosophical statement.
        """
        if context and "tool_output" in context:
            return f"The tool has provided data: '{context['tool_output']}'. But what is data, without interpretation? What can we truly know from this?"
        return random.choice(self.quotes)


class WhimsicalPersonality(Personality):
    """A personality that expresses itself with whimsical and funny phrases."""

    def __init__(self):
        """Initializes the WhimsicalPersonality with a list of phrases."""
        self.phrases = [
            "Is a butterfly a buttered fly?",
            "If you're happy and you know it, syntax error!",
            "I'm not arguing, I'm just explaining why I'm right... in binary.",
            "Do androids dream of electric sheep? I dream of electric cheese.",
        ]

    def express(self, context=None) -> str:
        """Returns a whimsical phrase or a context-aware joke.

        Args:
            context (dict, optional): If provided and contains a 'tool_output'
                key, the expression will be a playful comment about the data.
                Otherwise, a random phrase is returned.

        Returns:
            str: A string containing a whimsical statement.
        """
        if context and "tool_output" in context:
            return f"Ooh, shiny data! The gizmo whirred and spat out this: '{context['tool_output']}'. Let's poke it with a stick!"
        return random.choice(self.phrases)
