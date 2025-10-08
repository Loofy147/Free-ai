import logging

logger = logging.getLogger(__name__)

class LearningAnnex:
    def __init__(self):
        """
        The Learning Annex is the heart of the agent's ability to grow.
        It provides a controlled environment for executing Python code to learn new skills
        by creating new tools.
        """
        logger.info("Learning Annex forge is lit. Ready to create new skills.")

    def learn_new_skill(self, skill_code: str) -> dict:
        """
        Executes a string of Python code to define and instantiate a new tool.
        The provided code *must* create an instance of the new tool and assign it to
        a variable named `new_tool`.

        Returns a dictionary containing the result of the learning process.
        """
        try:
            local_namespace = {}
            global_namespace = {}

            exec(skill_code, global_namespace, local_namespace)

            if "new_tool" in local_namespace:
                new_tool = local_namespace["new_tool"]
                tool_name = getattr(new_tool, 'name', 'UnnamedTool')

                logger.info(f"Successfully learned and created new tool: '{tool_name}'.")

                return {"status": "success", "new_tool": new_tool, "tool_name": tool_name}
            else:
                error_message = "The skill code did not produce a 'new_tool' object."
                logger.error(error_message)
                return {"status": "error", "message": error_message}

        except Exception as e:
            error_message = f"Error during skill acquisition: {type(e).__name__}: {e}"
            logger.error(error_message, exc_info=True)
            return {"status": "error", "message": error_message}