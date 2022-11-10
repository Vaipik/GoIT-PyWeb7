import logging
from datetime import date, timedelta
import random

from faker import Faker

import db_operations


NAMES = tuple(Faker().name() for _ in range(random.randint(33, 50)))


def get_groups() -> list[str]:
    return ["PyDev-1", "PyDev-2", "PyDev-3"]


def get_subjects() -> list[str]:
    return ["Flask", "Django", "FastAPI", "DRF", "pandas", "NumPy"]


def get_student_names() -> tuple[str]:
    """
    According to condition there are only 3 tutors. Other names are for students.\n
    :return: tuple with students names
    """
    return NAMES[:-3]


def get_tutor_names() -> tuple[str]:
    """
    According to condition there are only 3 tutors. Their names are last in list.\n
    :return: tuple with tutor names
    """
    return NAMES[-3:]


def get_tutors_subject() -> dict[str]:
    """
    Giving tutors their subjects.\n
    :return: dictionary with subject as key and tutor as value.
    """
    return {subject: random.choice(get_tutor_names()) for subject in get_subjects()}


def get_mark() -> int:
    return random.randint(0, 100)


def get_date() -> str:
    current_date = date.today()
    previous_random_date = current_date - timedelta(random.randint(30, 40))
    return previous_random_date.strftime("%Y-%m-%d")


def split_students_to_groups() -> list[tuple[str, str]]:
    """
    Splitting students to groups.\n
    :return: List with tuples. The last contains group name and student name
    """
    students = set(get_student_names())
    students_count = len(students)
    groups = get_groups()
    result = []
    for group in groups:

        if students:
            students_in_group = set(random.sample(students, k=random.randint(10, students_count // len(groups))))
            for student in students_in_group:
                result.append((group, student))

            students -= students_in_group
    return result


def generate_marks(students_in_groups: list[tuple[str, str]]) -> list[tuple[str, str, str, int]]:
    """
    Generate data for marks table.\n
    :param students_in_groups: list with tuples. The last contains group name and student name.
    :return: list with tuples. Each tuple contains student name, subject name, marks date and finally mark.
    """
    subjects = get_subjects()
    return [(student[1], subject, get_date(), get_mark()) for _ in range(5) for subject in subjects for student in students_in_groups]


def generate_random_db_data(conn) -> None:
    """
    Filling all tables.\n
    :param conn: connection instance
    :return: None
    """
    tutors = [(tutor, ) for tutor in get_tutor_names()]  # type: list[tuple[str]]
    sql_to_tutors = """INSERT INTO tutors(tutor_name) VALUES(?);"""
    db_operations.insert_into_table(
        conn=conn,
        query=sql_to_tutors,
        data=tutors
    )

    tutors_subject = get_tutors_subject()  # type: dict[str: str]
    sql_to_subjects = """INSERT INTO subjects(subject_name, tutor_id)
    VALUES(?, (SELECT tutor_id FROM tutors WHERE tutor_name = ?))"""
    db_operations.insert_into_table(
        conn=conn,
        query=sql_to_subjects,
        data=list(tutors_subject.items())  # type: list[tuple[str, str]]
    )

    groups = [(group, ) for group in get_groups()]
    sql_to_groups = """INSERT INTO groups(group_name) VALUES(?)"""
    db_operations.insert_into_table(
        conn=conn,
        query=sql_to_groups,
        data=groups
    )

    students_in_groups = split_students_to_groups()  # type: list[tuple[str, str]]
    sql_to_students = """INSERT INTO students(group_id, student_name)
    VALUES((SELECT group_id FROM groups WHERE group_name = ?), ?)"""
    db_operations.insert_into_table(
        conn=conn,
        query=sql_to_students,
        data=students_in_groups
    )

    marks = generate_marks(students_in_groups)
    sql_to_marks = """INSERT INTO marks(student_id, subject_id, date_received, result)
    VALUES(
        (SELECT student_id FROM students WHERE student_name = ?),
        (SELECT subject_id FROM subjects WHERE subject_name = ?),
        ?,
        ?);"""
    db_operations.insert_into_table(
        conn=conn,
        query=sql_to_marks,
        data=marks
    )
