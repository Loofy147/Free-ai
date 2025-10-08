import logging
import uuid
import time
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class Agora:
    """
    The Agora is the central message board for the agent society.
    It allows agents to post tasks and retrieve results for collaboration.
    """
    def __init__(self):
        self.message_board: List[Dict] = []
        logger.info("The Agora is now open.")

    def post_message(self, from_agent: str, to_agent_role: str, content: Dict) -> str:
        """
        Posts a new message (task) to the message board.
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
        """
        Retrieves all unclaimed messages targeted at a specific role.
        """
        unclaimed = [
            msg for msg in self.message_board
            if msg["to_agent_role"] == role and msg["claimed_by"] is None
        ]
        logger.info(f"Found {len(unclaimed)} unclaimed messages for role '{role}'.")
        return unclaimed

    def claim_message(self, message_id: str, by_agent: str):
        """
        Marks a message as claimed by a specific agent.
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
        """
        Posts a reply to a previously claimed message.
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
        """
        Checks for a reply to a specific message ID.
        """
        for msg in self.message_board:
            if msg["id"] == message_id:
                return msg.get("reply")
        return None