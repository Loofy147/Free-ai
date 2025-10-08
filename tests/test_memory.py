import os
import sys
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from free_ai.memory import VectorMemory

@pytest.fixture
def memory_instance(tmp_path):
    """
    A pytest fixture to create a fresh, isolated VectorMemory instance for each test
    using pytest's built-in tmp_path fixture.
    """
    db_path = tmp_path / "test_memory_db"
    memory = VectorMemory(path=str(db_path))
    # No cleanup needed, pytest handles the tmp_path directory.
    yield memory

def test_add_and_query_memory(memory_instance):
    """
    Tests that text can be added to memory and then retrieved
    via a semantically similar query.
    """
    # 1. Define the knowledge to be added
    knowledge_to_add = "The SOLID principles are a set of five design principles in object-oriented programming intended to make software designs more understandable, flexible, and maintainable."

    # 2. Add the knowledge to the memory
    memory_instance.add(knowledge_to_add)

    # 3. Formulate a query that is semantically similar
    query = "What are the design principles for good software?"

    # 4. Query the memory
    results = memory_instance.query(query, n_results=1)

    # 5. Assert that the results are as expected
    assert len(results) == 1, "The query should return exactly one result."
    assert "SOLID principles" in results[0], "The retrieved document should contain the original knowledge."

def test_query_empty_memory(memory_instance):
    """
    Tests that querying an empty memory returns an empty list.
    """
    query = "What is the meaning of life?"
    results = memory_instance.query(query)

    assert results == [], "Querying an empty memory should return an empty list."

def test_add_increases_document_count(memory_instance):
    """
    Tests that adding a document increases the count of items in the collection.
    """
    initial_count = memory_instance.collection.count()
    assert initial_count == 0, "The collection should be empty initially."

    memory_instance.add("This is a test document.")

    new_count = memory_instance.collection.count()
    assert new_count == 1, "The collection count should be 1 after adding a document."