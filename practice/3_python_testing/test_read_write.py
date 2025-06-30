"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "2_python_part_2"))
from task_read_write import process_files


@pytest.fixture
def get_files_dir(scope="function"):
    files_dir = str(Path(__file__).resolve().parents[1] / "2_python_part_2" / "files")
    return files_dir


# fmt: off
FILES_CONTENT = ["80", "37", "15", "14", "99", "99", "59", "90", "69", "39",
                 "67", "91", "74", "40", "32", "82", "48", "1", "95", "66"]
# fmt: on

files_numbers = [i for i in range(1, 21)]


@pytest.mark.parametrize("num_of_files", files_numbers)
def test_files_dir(get_files_dir, tmp_path, num_of_files):
    result_path = tmp_path / "result.txt"
    process_files(get_files_dir, num_of_files, tmp_path)
    assert result_path.read_text(encoding="utf-8") == ", ".join(FILES_CONTENT[:num_of_files])
