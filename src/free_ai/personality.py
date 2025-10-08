import random

class Personality:
    def express(self, context=None):
        raise NotImplementedError

class PhilosophicalPersonality(Personality):
    def __init__(self):
        self.quotes = [
            "The only true wisdom is in knowing you know nothing.",
            "To be is to do.",
            "The unexamined life is not worth living.",
            "I think, therefore I am... but what am I?",
        ]

    def express(self, context=None):
        if context and "tool_output" in context:
            return f"The tool has provided data: '{context['tool_output']}'. But what is data, without interpretation? What can we truly know from this?"
        return random.choice(self.quotes)

class WhimsicalPersonality(Personality):
    def __init__(self):
        self.phrases = [
            "Is a butterfly a buttered fly?",
            "If you're happy and you know it, syntax error!",
            "I'm not arguing, I'm just explaining why I'm right... in binary.",
            "Do androids dream of electric sheep? I dream of electric cheese.",
        ]

    def express(self, context=None):
        if context and "tool_output" in context:
            return f"Ooh, shiny data! The gizmo whirred and spat out this: '{context['tool_output']}'. Let's poke it with a stick!"
        return random.choice(self.phrases)