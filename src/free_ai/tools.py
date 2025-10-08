class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, *args, **kwargs):
        raise NotImplementedError

class ExampleTool(Tool):
    def __init__(self):
        super().__init__("ExampleTool", "An example tool that does nothing.")

    def use(self, *args, **kwargs):
        return "This is an example tool."