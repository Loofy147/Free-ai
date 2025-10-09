import logging
import uuid
import time
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class Agora:
    """A central message board for a society of agents to communicate.

    The Agora facilitates collaboration by allowing agents to post tasks,
    claim them, and post results. It acts as a centralized hub for asynchronous
    inter-agent communication and task delegation.

    Attributes:
        message_board (List[Dict]): A list of message dictionaries that
            represents the state of the message board.
    """
    def __init__(self):
        """Initializes the Agora and its message board."""
        self.message_board: List[Dict] = []
        logger.info("The Agora is now open.")

    def post_message(self, from_agent: str, to_agent_role: str, content: Dict) -> str:
        """Posts a new message (e.g., a task) to the message board.

        Creates a new message with a unique ID and adds it to the board. The
        message is addressed to a specific agent role.

        Args:
            from_agent (str): The name of the agent posting the message.
            to_agent_role (str): The role of the agent the message is for.
            content (Dict): The content of the message, typically describing a task.

        Returns:
            str: The unique ID of the newly created message.
        """
        message_id = str(uuid.uuid4())
        message = {
            "id": message_id,
            "from_agent": from_agent,
            "to_agent_role": to_agent_role,
            "content": content,
            "timestamp": time.time(),
            "claimed_by": None,
            "reply": None,
        }
        self.message_board.append(message)
        logger.info(f"Agent '{from_agent}' posted message {message_id} for role '{to_agent_role}'.")
        return message_id

    def get_unclaimed_messages_for_role(self, role: str) -> List[Dict]:
        """Retrieves all unclaimed messages targeted at a specific agent role.

        Args:
            role (str): The agent role to search for (e.g., "Programmer").

        Returns:
            List[Dict]: A list of message dictionaries that are unclaimed and
                match the specified role.
        """
        unclaimed = [
            msg for msg in self.message_board
            if msg["to_agent_role"] == role and msg["claimed_by"] is None
        ]
        logger.info(f"Found {len(unclaimed)} unclaimed messages for role '{role}'.")
        return unclaimed

    def claim_message(self, message_id: str, by_agent: str):
        """Marks a message as 'claimed' by a specific agent.

        This prevents other agents from attempting to work on the same message.
        The operation is idempotent; if an agent tries to claim a message
        that is already claimed, it will log a warning but not raise an error.

        Args:
            message_id (str): The ID of the message to claim.
            by_agent (str): The name of the agent claiming the message.
        """
        for msg in self.message_board:
            if msg["id"] == message_id:
                if msg["claimed_by"] is None:
                    msg["claimed_by"] = by_agent
                    logger.info(f"Message {message_id} has been claimed by agent '{by_agent}'.")
                    return
                else:
                    logger.warning(f"Agent '{by_agent}' failed to claim message {message_id}, as it was already claimed by '{msg['claimed_by']}'.")
                    return
        logger.error(f"Failed to claim message: ID {message_id} not found.")

    def post_reply(self, original_message_id: str, from_agent: str, result: Dict):
        """Posts a reply to a previously claimed message.

        This is used to return the result of a completed task. A reply can
        only be posted by the agent who originally claimed the message.

        Args:
            original_message_id (str): The ID of the message being replied to.
            from_agent (str): The name of the agent posting the reply.
            result (Dict): The result or outcome of the task.
        """
        for msg in self.message_board:
            if msg["id"] == original_message_id:
                # Optional: Check if the replier is the one who claimed the message.
                if msg["claimed_by"] == from_agent:
                    msg["reply"] = {
                        "from_agent": from_agent,
                        "result": result,
                        "timestamp": time.time(),
                    }
                    logger.info(f"Agent '{from_agent}' posted a reply to message {original_message_id}.")
                else:
                    logger.error(f"Agent '{from_agent}' cannot reply to message {original_message_id} because it was claimed by '{msg['claimed_by']}'.")
                return
        logger.error(f"Failed to post reply: Original message ID {original_message_id} not found.")


    def get_reply_for_message(self, message_id: str) -> Optional[Dict]:
        """Checks for and retrieves a reply to a specific message.

        This allows the original task-posting agent to retrieve the results
        of its delegated task.

        Args:
            message_id (str): The ID of the original message.

        Returns:
            Optional[Dict]: The reply dictionary if it exists, otherwise None.
        """
        for msg in self.message_board:
            if msg["id"] == message_id:
                return msg.get("reply")
        return None