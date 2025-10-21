import logging

logger = logging.getLogger(__name__)


class LearningAnnex:
    """A module for dynamically learning new skills by executing code.

    The Learning Annex provides a controlled environment for an agent to
    expand its capabilities. It can execute a string of Python code, which is
    expected to define and instantiate a new tool. This allows the agent to
    create and integrate new functionalities at runtime.
    """

    def __init__(self):
        """Initializes the Learning Annex."""
        logger.info("Learning Annex forge is lit. Ready to create new skills.")

    def learn_new_skill(self, skill_code: str) -> dict:
        """Executes Python code to define and instantiate a new tool.

        This method uses `exec` to run the provided code. The code must
        create an instance of a new tool class and assign it to a variable
        named `new_tool` in the local namespace.

        Args:
            skill_code (str): A string containing the Python code for the new skill.

        Returns:
            dict: A dictionary containing the result of the operation.
                On success, it includes `{'status': 'success', 'new_tool': ...,
                'tool_name': ...}`.
                On failure, it includes `{'status': 'error', 'message': ...}`.
        """
        try:
            local_namespace = {}
            global_namespace = {}

            exec(skill_code, global_namespace, local_namespace)

            if "new_tool" in local_namespace:
                new_tool = local_namespace["new_tool"]
                tool_name = getattr(new_tool, "name", "UnnamedTool")

                logger.info(
                    f"Successfully learned and created new tool: '{tool_name}'."
                )

                return {
                    "status": "success",
                    "new_tool": new_tool,
                    "tool_name": tool_name,
                }
            else:
                error_message = "The skill code did not produce a 'new_tool' object."
                logger.error(error_message)
                return {"status": "error", "message": error_message}

        except Exception as e:
            error_message = f"Error during skill acquisition: {type(e).__name__}: {e}"
            logger.error(error_message, exc_info=True)
            return {"status": "error", "message": error_message}
