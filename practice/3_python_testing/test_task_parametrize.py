"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal in the Fibonacci sequence.
One of them has a bug.

Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number

Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""

import pytest


def fibonacci_1(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_2(n):
    fibo = [0, 1]
    for i in range(2, n + 1):
        fibo.append(fibo[i - 1] + fibo[i - 2])
    return fibo[n]


fibonacci_seq = [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (7, 13),
    (8, 21),
    (9, 34),
    (10, 55),
    (11, 89),
    (12, 144),
    (13, 233),
    (14, 377),
    (15, 610),
    (16, 987),
    (17, 1597),
    (18, 2584),
    (19, 4181),
]


@pytest.mark.parametrize("func, index, result", fibonacci_seq)
def test_fibonacci_1(index, result):
    assert fibonacci_1(index) == result


@pytest.mark.parametrize("index, result", fibonacci_seq)
def test_fibonacci_2(index, result):
    assert fibonacci_1(index) == result
