"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import datetime
import sys
from pathlib import Path

import pytest
from freezegun import freeze_time

sys.path.append(str(Path(__file__).resolve().parents[1] / "2_python_part_2"))
from task_classes import Homework, Student, Teacher


@pytest.fixture
def teacher(scope="function"):
    yield Teacher("Dmitry", "Orlyakov")


@pytest.fixture
def student(scope="function"):
    yield Student("Vladislav", "Popov")


def test_teacher_init(teacher):
    assert teacher.last_name == "Dmitry"
    assert teacher.first_name == "Orlyakov"


def test_student_init(student):
    assert student.last_name == "Vladislav"
    assert student.first_name == "Popov"


@freeze_time("2025-06-30 12:00:00")
def test_create_expired_homework(teacher):
    expired_homework = teacher.create_homework("Learn functions", 0)
    assert expired_homework.created == datetime.datetime(2025, 6, 30, 12, 0, 0)
    assert expired_homework.deadline == datetime.timedelta(days=0)
    assert expired_homework.text == "Learn functions"
    assert expired_homework.is_active() is False


@freeze_time("2025-06-30 12:00:00")
def test_create_normal_homework(teacher):
    normal_homework = teacher.create_homework("Learn functions", 2)
    assert normal_homework.created == datetime.datetime(2025, 6, 30, 12, 0, 0)
    assert normal_homework.deadline == datetime.timedelta(days=2)
    assert normal_homework.text == "Learn functions"
    assert normal_homework.is_active() is True


def test_student_do_homework(capfd, teacher, student):
    homework = teacher.create_homework("Create 2 simple classes", 5)
    result = student.do_homework(homework)
    out, err = capfd.readouterr()
    assert result == homework
    assert out == ""


def test_student_do_expired_homework(capfd, teacher, student):
    homework = teacher.create_homework("Create 2 simple classes", 0)
    result = student.do_homework(homework)
    out, err = capfd.readouterr()
    assert result is None
    assert out == "You are late\n"
