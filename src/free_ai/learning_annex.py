class LearningAnnex:
    def __init__(self):
        """
        The Learning Annex is the heart of the agent's ability to grow.
        It provides a controlled environment for executing Python code to learn new skills
        by creating new tools.
        """
        print("LEARNING ANNEX: Forge is lit. Ready to create new skills.")

    def learn_new_skill(self, skill_code: str) -> dict:
        """
        Executes a string of Python code to define and instantiate a new tool.
        The provided code *must* create an instance of the new tool and assign it to
        a variable named `new_tool`.

        Returns a dictionary containing the result of the learning process.
        """
        try:
            # Create a dedicated local namespace for the execution to run in.
            # This is a security measure to prevent the code from overwriting
            # existing variables in the agent's environment.
            local_namespace = {}

            # The global namespace can be kept simple for now.
            global_namespace = {}

            # Execute the code provided by the Cognitive Engine.
            exec(skill_code, global_namespace, local_namespace)

            # The contract with the Cognitive Engine is that it must create a 'new_tool' variable.
            if "new_tool" in local_namespace:
                new_tool = local_namespace["new_tool"]
                tool_name = getattr(new_tool, 'name', 'UnnamedTool')

                print(f"LEARNING ANNEX: Successfully learned and created new tool: '{tool_name}'.")

                # Return the new tool so the Body can add it to its list of capabilities.
                return {"status": "success", "new_tool": new_tool, "tool_name": tool_name}
            else:
                error_message = "The skill code did not produce a 'new_tool' object."
                print(f"LEARNING ANNEX: Error - {error_message}")
                return {"status": "error", "message": error_message}

        except Exception as e:
            error_message = f"Error during skill acquisition: {type(e).__name__}: {e}"
            print(f"LEARNING ANNEX: Error - {error_message}")
            return {"status": "error", "message": error_message}