"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""

import math

import pytest


class OperationNotFoundException(Exception):
    pass


def math_calculate(function: str, *args):
    """Wrapper for 'math' module which allows calculations with maxiumum of 2 arguments"""
    if len(args) > 2:
        raise OperationNotFoundException("Only operations with 1 or 2 arguments are allowed")
    try:
        math_function = getattr(math, function)
        return math_function(*args)
    except AttributeError as err:
        raise OperationNotFoundException(err)


"""
Write tests for math_calculate function
"""


def test_log_calculate():
    assert math_calculate("log", 1024, 2) == 10.0


def test_ceil_calculate():
    assert math_calculate("ceil", 10.7) == 11


def test_operation_with_more_arguments():
    with pytest.raises(OperationNotFoundException) as excinfo:
        math_calculate("fma", 10, 12, 2)
    assert str(excinfo.value) == "Only operations with 1 or 2 arguments are allowed"


def test_operation_not_found():
    with pytest.raises(OperationNotFoundException):
        math_calculate("dot", 10, 12)
