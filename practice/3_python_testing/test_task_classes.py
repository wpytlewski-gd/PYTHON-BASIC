"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import datetime
import sys
from pathlib import Path

import pytest

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


def test_create_homework(teacher):
    # TODO: write this test correctly and check time created somehow:
    # Maybe you can mock a time module somehow
    expired_homework = teacher.create_homework("Learn functions", 0)
    assert expired_homework.deadline == datetime.timedelta(0)
    assert expired_homework.text == "Learn functions"
    assert expired_homework.is_active() is False


def test_create_normal_homework(teacher):
    # TODO: write this test correctly and check time created somehow:
    # Maybe you can mock a time module somehow
    normal_homework = teacher.create_homework("Learn functions", 2)
    assert normal_homework.deadline == datetime.timedelta(2)
    assert normal_homework.text == "Learn functions"
    assert normal_homework.is_active() is True


def test_student_do_homework(teacher, student):
    homework = teacher.create_homework("Create 2 simple classes", 5)
    assert student.do_homework(homework) == homework


def test_student_do_expired_homework(teacher, student):
    homework = teacher.create_homework("Create 2 simple classes", 0)
    assert student.do_homework(homework) is None
