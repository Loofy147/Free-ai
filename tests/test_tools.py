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

@pytest.fixture
def temp_dir_structure(tmp_path):
    """A pytest fixture to create a temporary directory structure for testing."""
    base_dir = tmp_path / "test_dir"
    base_dir.mkdir()
    (base_dir / "file1.txt").write_text("file1")

    sub_dir = base_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "file2.txt").write_text("file2")

    return str(base_dir)

def test_filesystemtool_list_recursive_success(temp_dir_structure):
    """
    Tests that the FileSystemTool can successfully list files and directories recursively.
    """
    base_dir = temp_dir_structure
    tool = FileSystemTool()

    result = tool.use(operation="list_recursive", path=base_dir)

    assert result["status"] == "success"

    expected_files = [
        "file1.txt",
        "subdir/",
        "subdir/file2.txt"
    ]
    # The implementation sorts the list, so we should compare against a sorted list.
    expected_files.sort()

    # The result from the tool should also be sorted.
    assert result["files"] == expected_files