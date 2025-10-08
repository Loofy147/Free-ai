import os
import sys
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from free_ai.agora import Agora

@pytest.fixture
def agora_instance():
    """A pytest fixture to create a fresh Agora instance for each test."""
    return Agora()

def test_post_and_get_message(agora_instance):
    """
    Tests that a message can be posted and then retrieved by an agent with the correct role.
    """
    # 1. Post a message from a "Manager" to any agent with the "Researcher" role.
    task_content = {"task": "research SOLID principles"}
    message_id = agora_instance.post_message(from_agent="Manager_1", to_agent_role="Researcher", content=task_content)

    assert message_id is not None, "Posting a message should return a unique message ID."

    # 2. A "Researcher" agent should see this message.
    researcher_messages = agora_instance.get_unclaimed_messages_for_role("Researcher")
    assert len(researcher_messages) == 1
    assert researcher_messages[0]['id'] == message_id
    assert researcher_messages[0]['content'] == task_content

    # 3. A "Coder" agent should NOT see this message.
    coder_messages = agora_instance.get_unclaimed_messages_for_role("Coder")
    assert len(coder_messages) == 0

def test_message_claiming(agora_instance):
    """
    Tests that a message can be claimed and is no longer available to others.
    """
    # 1. Post a message.
    task_content = {"task": "find the 'D' in SOLID"}
    message_id = agora_instance.post_message(from_agent="Manager_1", to_agent_role="Researcher", content=task_content)

    # 2. A "Researcher" claims the message.
    agora_instance.claim_message(message_id, by_agent="Researcher_A")

    # 3. The message should no longer be in the unclaimed list for any researcher.
    unclaimed_messages = agora_instance.get_unclaimed_messages_for_role("Researcher")
    assert len(unclaimed_messages) == 0

def test_post_and_get_reply(agora_instance):
    """
    Tests that a reply can be posted to a claimed message and retrieved by the original sender.
    """
    # 1. Post and claim a message.
    task_content = {"task": "what is dependency inversion?"}
    message_id = agora_instance.post_message(from_agent="Manager_1", to_agent_role="Researcher", content=task_content)
    agora_instance.claim_message(message_id, by_agent="Researcher_B")

    # 2. Check that there is no reply yet.
    reply = agora_instance.get_reply_for_message(message_id)
    assert reply is None, "There should be no reply initially."

    # 3. The "Researcher" posts a reply.
    reply_content = {"answer": "The 'D' in SOLID stands for Dependency Inversion Principle."}
    agora_instance.post_reply(message_id, from_agent="Researcher_B", result=reply_content)

    # 4. The original sender should now be able to retrieve the reply.
    final_reply = agora_instance.get_reply_for_message(message_id)
    assert final_reply is not None
    assert final_reply['result'] == reply_content
    assert final_reply['from_agent'] == "Researcher_B"