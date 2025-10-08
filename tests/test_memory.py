import os
import sys
import pytest
import shutil

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from free_ai.memory import VectorMemory

# Define a temporary path for the test database that persists across fixtures
TEST_DB_PATH = "./test_collective_memory_db"

@pytest.fixture(scope="module")
def persistent_memory_path():
    """A module-scoped fixture to ensure the db path is the same for relevant tests."""
    # Clean up before the first test in the module
    if os.path.exists(TEST_DB_PATH):
        shutil.rmtree(TEST_DB_PATH)

    yield TEST_DB_PATH

    # Clean up after all tests in the module are done
    if os.path.exists(TEST_DB_PATH):
        shutil.rmtree(TEST_DB_PATH)

def test_add_and_query_in_separate_sessions(persistent_memory_path):
    """
    The core test for Project Mnemosyne.
    Tests that knowledge added by one memory instance is persistent and can be
    retrieved by a completely new instance.
    """
    # --- Session 1: The Researcher Agent ---
    memory_session_1 = VectorMemory(path=persistent_memory_path)
    knowledge_to_add = "The Liskov Substitution Principle states that objects of a superclass shall be replaceable with objects of a subclass without affecting the correctness of the program."
    memory_session_1.add(knowledge_to_add, metadata={"source": "Researcher-Gamma"})

    # --- Session 2: The Manager Agent ---
    # We create a completely new instance, connecting to the same persistent storage.
    memory_session_2 = VectorMemory(path=persistent_memory_path)
    query = "What is the 'L' in SOLID?"

    results = memory_session_2.query(query, n_results=1)

    # Assert that the second agent can recall the first agent's knowledge.
    assert len(results) == 1, "The query should retrieve the document stored in the previous session."
    assert "Liskov Substitution Principle" in results[0], "The retrieved document should contain the correct information."

def test_add_increases_document_count(persistent_memory_path):
    """
    Tests that adding a document correctly increases the item count.
    This test relies on the state from the previous test in this module.
    """
    # This test is intentionally simple and builds on the previous one.
    # We expect one document from the test above.
    memory = VectorMemory(path=persistent_memory_path)
    assert memory.collection.count() == 1, "The collection count should be 1 from the previous test."

    memory.add("Another test document.")

    assert memory.collection.count() == 2, "The collection count should be 2 after adding a new document."

def test_query_empty_memory(tmp_path):
    """
    Tests that querying a completely separate, empty memory returns an empty list.
    Uses tmp_path to ensure it's a different database.
    """
    db_path = tmp_path / "empty_db"
    memory = VectorMemory(path=str(db_path))
    query = "What is the meaning of life?"
    results = memory.query(query)

    assert results == [], "Querying an empty memory should return an empty list."