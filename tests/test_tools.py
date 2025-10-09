import os
import sys
import pytest

# Add the src directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from free_ai.tools import FileSystemTool

@pytest.fixture
def temp_file(tmp_path):
    """A pytest fixture to create a temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_content = "Hello, world!"
    file_path.write_text(file_content)
    return file_path, file_content

def test_filesystemtool_read_file_success(temp_file):
    """
    Tests that the FileSystemTool can successfully read a file.
    """
    file_path, expected_content = temp_file
    tool = FileSystemTool()

    result = tool.use(operation="read_file", filepath=str(file_path))

    assert result["status"] == "success"
    assert expected_content in result["content"]

def test_filesystemtool_read_file_not_found():
    """
    Tests that the FileSystemTool gracefully handles a file not found error.
    """
    tool = FileSystemTool()

    result = tool.use(operation="read_file", filepath="non_existent_file.txt")

    assert result["status"] == "error"
    assert "File not found" in result["message"]