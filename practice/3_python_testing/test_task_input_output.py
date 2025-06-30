"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""

import io
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "2_python_part_2"))
from task_input_output import read_numbers


@patch("sys.stdin", new=io.StringIO("1\n2\n3\n4\n5"))
def test_read_numbers_without_text_input():
    assert read_numbers(4) == "Avg: 2.50"


@patch("sys.stdin", new=io.StringIO("1\n2\nText"))
def test_read_numbers_with_text_input():
    assert read_numbers(3) == "Avg: 1.50"


@patch("sys.stdin", new=io.StringIO("hello\nworld\nfoo\nbar\nbaz"))
def test_read_numbers_without_numbers():
    assert read_numbers(3) == "No numbers entered"
