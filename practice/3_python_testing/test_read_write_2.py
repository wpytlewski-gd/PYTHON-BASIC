"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "2_python_part_2"))
from task_read_write_2 import main as task_main

words = [
    "oqh",
    "zxlzsyvprl",
    "pdbhthpkit",
    "mjgasq",
    "icqfu",
    "ell",
    "illuh",
    "dxfamdctiu",
    "prym",
    "dhovdkrhg",
    "btqcxrweaf",
    "mkcirx",
    "cwnikvmdpv",
    "twc",
    "puxqi",
    "slaxgt",
    "zxmmeuwm",
    "mzrzi",
    "kllibqge",
    "dlxs",
]


@patch("task_read_write_2.generate_words", return_value=words)
def test_generate_words_utf_8(mock_input, tmp_path):
    task_main(tmp_path)
    utf8_file_path = tmp_path / "results_utf8.txt"
    expected_content = "\n".join(words)
    assert utf8_file_path.exists()
    assert utf8_file_path.read_text() == expected_content


@patch("task_read_write_2.generate_words", return_value=words)
def test_generate_words_cp1252(mock_input, tmp_path):
    task_main(tmp_path)
    cp1252_file_path = tmp_path / "results_cp1252.txt"
    expected_content = ",".join(reversed(words))
    assert cp1252_file_path.exists()
    assert cp1252_file_path.read_text(encoding="cp1252") == expected_content
