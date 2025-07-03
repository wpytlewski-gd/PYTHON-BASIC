"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""

from datetime import datetime

import pytest
from freezegun import freeze_time


class WrongFormatException(Exception):
    pass


def calculate_days(from_date: str) -> int:
    try:
        datetime_from_date = datetime.fromisoformat(from_date)
    except ValueError as err:
        raise WrongFormatException(err)
    now = datetime.now()
    days_diff = now - datetime_from_date
    return int(days_diff.days)


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""


@freeze_time("2025-07-02 12:00:00")
def test_calculate_same_day():
    assert calculate_days("2025-07-02") == 0


@freeze_time("2025-07-02 12:00:00")
def test_calculate_positive_days():
    assert calculate_days("2025-06-30") == 2


@freeze_time("2025-07-02 12:00:00")
def test_calculate_negative_days():
    assert calculate_days("2025-07-03") == -1


@freeze_time("2025-07-02 12:00:00")
def test_calculate_positive_year():
    assert calculate_days("2024-07-02") == 365


@freeze_time("2025-07-02 12:00:00")
def test_calculate_negative_year():
    assert calculate_days("2026-07-02") == -365


@freeze_time("2024-03-10")
def test_calculate_days_leap_year():
    assert calculate_days("2023-03-10") == 366


def test_wrong_format_separator():
    with pytest.raises(WrongFormatException):
        calculate_days("2024,07,02")


def test_wrong_format_months_days_changed():
    with pytest.raises(WrongFormatException):
        calculate_days("2024-25-03")


def test_random_string():
    with pytest.raises(WrongFormatException):
        calculate_days("fsafSD#$%^&!@fas")
