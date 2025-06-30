"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""

import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "2_python_part_2"))
from task_exceptions import DivisionByOneException, division


def test_division_ok(capfd):
    out_value = division(2, 2)
    out, err = capfd.readouterr()
    assert out == "Division finished\n"
    assert out_value == 1


def test_division_by_zero(capfd):
    out_value = division(1, 0)
    out, err = capfd.readouterr()
    assert out == "Division by 0\nDivision finished\n"
    assert out_value is None


def test_division_by_one(capfd):
    with pytest.raises(DivisionByOneException) as excinfo:
        division(1, 1)
    out, err = capfd.readouterr()
    assert out == "Division finished\n"
    assert "Division on 1 get the same result" in str(excinfo.value)
