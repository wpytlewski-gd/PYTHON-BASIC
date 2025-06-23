"""
Create 3 classes with interconnection between them (Student, Teacher,
Homework)
Use datetime module for working with date/time
1. Homework takes 2 attributes for __init__: tasks text and number of days to complete
Attributes:
    text - task text
    deadline - datetime.timedelta object with date until task should be completed
    created - datetime.datetime object when the task was created
Methods:
    is_active - check if task already closed
2. Student
Attributes:
    last_name
    first_name
Methods:
    do_homework - request Homework object and returns it,
    if Homework is expired, prints 'You are late' and returns None
3. Teacher
Attributes:
     last_name
     first_name
Methods:
    create_homework - request task text and number of days to complete, returns Homework object
    Note that this method doesn't need object itself
PEP8 comply strictly.
"""

import datetime
from typing import Optional


class Homework:
    """Represents a homework task with a creation date and deadline.

    Attributes:
        text (str): The text description of the homework task.
        deadline (datetime.timedelta): The duration given to complete the task.
        created (datetime.datetime): The timestamp when the task was created.
    """

    def __init__(self, text: str, days_to_complete: int) -> None:
        """Initializes a Homework instance.

        Args:
            text: The text description of the task.
            days_to_complete: The number of days given to complete the task.
        """
        self.text = text
        self.deadline = datetime.timedelta(days_to_complete)
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        """Checks if the homework deadline has passed.

        Returns:
            True if the deadline has not yet been reached, otherwise False.
        """
        return self.created + self.deadline > datetime.datetime.now()


class Teacher:
    """Represents a teacher who can create Homework.

    Attributes:
        last_name (str): The last name of the teacher.
        first_name (str): The first name of the teacher.
    """

    def __init__(self, last_name: str, first_name: str) -> None:
        """Initializes a Teacher instance.

        Args:
            last_name: The last name of the teacher.
            first_name: The first name of the teacher.
        """
        self.last_name = last_name
        self.first_name = first_name

    @staticmethod
    def create_homework(text: str, days: int) -> Homework:
        """A factory method to create Homework instances.

        Args:
            text: The text description for the new homework.
            days: The number of days the student has to complete it.

        Returns:
            A new Homework object.
        """
        return Homework(text, days)


class Student:
    """Represents a student who can perform Homework.

    Attributes:
        last_name (str): The last name of the student.
        first_name (str): The first name of the student.
    """

    def __init__(self, last_name: str, first_name: str) -> None:
        """Initializes a Student instance.

        Args:
            last_name: The last name of the student.
            first_name: The first name of the student.
        """
        self.last_name = last_name
        self.first_name = first_name

    def do_homework(self, homework: Homework) -> Optional[Homework]:
        """Performs a homework task if it is still active.

        Args:
            homework: The Homework object to perform.

        Returns:
            The Homework object if it's not expired, otherwise None.
        """
        if not homework.is_active():
            print("You are late")
            return None
        return homework


if __name__ == "__main__":
    teacher = Teacher("Dmitry", "Orlyakov")
    student = Student("Vladislav", "Popov")
    print(teacher.last_name)  # Dmitry
    print(student.first_name)  # Popov

    expired_homework = teacher.create_homework("Learn functions", 0)
    print(expired_homework.created)  # Example: 2019-05-26 16:44:30.688762
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # 'Learn functions'

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too("create 2 simple classes", 5)
    print(oop_homework.deadline)  # 5 days, 0:00:00

    print(student.do_homework(oop_homework))
    student.do_homework(expired_homework)  # You are late
