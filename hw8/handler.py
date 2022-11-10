import logging
from pathlib import Path
import sqlite3

import data_generation
import db_operations

BASE_DIR = Path(__file__).parent


def five_max_avg(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Five students with the highest total average result.\n
    :param conn: db connection instance
    :return: list with affected rows
    """
    with conn:

        try:
            result = conn.execute("""SELECT student_name, ROUND(AVG(result), 2) AS average FROM
            marks
                INNER JOIN students USING(student_id)
            GROUP BY student_name
            HAVING students.student_id = marks.student_id
            ORDER BY average DESC
            LIMIT 5;""")

            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def one_max_avg(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    One student who has the highest average result on the desired subject.\n
    :param conn: db connection instance
    :return: list with affected rows
    """
    subject_name = input(">>> Enter subject: ")
    with conn:

        try:
            result = conn.execute("""SELECT student_name, subject_name, AVG(result) AS average FROM
                                    subjects
                                        INNER JOIN marks USING(subject_id)
                                        INNER JOIN students USING(student_id)
                                    GROUP BY student_name, subject_name
                                    HAVING subject_name = ?
                                    ORDER BY average DESC
                                    LIMIT 1;""", (subject_name,))
            return result.description, result.fetchall()
        except Exception as e:
            logging.error(e)


def avg_subject_in_group(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Average result for given subject and group.\n
    :param conn: db connection instance
    :return: list with affected rows
    """
    subject_name = input(">>> Enter subject: ").strip()
    group_name = input(">>> Enter group: ").strip()

    with conn:

        try:
            result = conn.execute(
                """SELECT group_name, subject_name, AVG(result) AS average FROM
                    subjects 
                        INNER JOIN marks USING(subject_id)
                        INNER JOIN students USING(student_id)
                        INNER JOIN groups USING(group_id)
                    GROUP BY group_name, subject_name
                    HAVING subject_name = ? AND group_name = ?
                    ORDER BY average DESC;""",
                (subject_name, group_name)
            )
            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def avg_on_course(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Total average marks for one course.\n
    :param conn: db connection instance
    :return: list with affected rows
    """
    with conn:

        try:
            result = conn.execute("""SELECT ROUND(AVG(result), 2) AS average FROM marks;""")
            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def tutor_subjects(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Tutor with his/her subjects.\n
    :param conn: db connection instance.
    :return: list of affected rows
    """
    tutor_name = input(">>> Enter tutor: ").strip()
    try:

        with conn:
            result = conn.execute(
                """SELECT tutor_name, subject_name FROM
                tutors	INNER JOIN subjects USING(tutor_id)
                WHERE tutor_name = ?;""",
                (tutor_name,)
            )
            return result.description, result.fetchall()

    except Exception as e:
        logging.error(e)


def students_in_group(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    All students in group.\n
    :param conn: db connection instance
    :return: list of affected rows.
    """
    group_name = input(">>> Enter group: ").strip()

    with conn:

        try:
            result = conn.execute(
                """SELECT student_name, group_name FROM
                groups
                    INNER JOIN students USING(group_id)
                WHERE group_name = ?;""",
                (group_name,)
            )

            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def students_marks_by_group_and_subject(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Student marks for desired group and subject.\n
    :param conn: db connection instance.
    :return: list of affected rows.
    """
    subject_name = input(">>> Enter subject: ").strip()
    group_name = input(">>> Enter group: ").strip()

    with conn:

        try:
            result = conn.execute(
                """SELECT student_name, group_name, subject_name, result FROM
                subjects
                    INNER JOIN marks USING(subject_id)
                    INNER JOIN students USING(student_id)
                    INNER JOIN groups USING(group_id)
                WHERE subject_name = ? AND group_name = ?
                ORDER BY student_name;
                """,
                (subject_name, group_name)
            )
            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def last_lesson_marks(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Marks for one group last lesson.\n
    :param conn: db connection instance.
    :return: list of affected rows.
    """
    subject_name = input(">>> Enter subject: ").strip()
    group_name = input(">>> Enter group: ").strip()

    with conn:

        try:
            result = conn.execute(
                """SELECT student_name, group_name, subject_name, result, date_received FROM
                subjects
                    INNER JOIN marks USING(subject_id)
                    INNER JOIN students USING(student_id)
                    INNER JOIN groups USING(group_id)
                WHERE subject_name = ? AND group_name = ? AND date_received = (SELECT MAX(date_received) FROM marks)
                ORDER BY date_received DESC;
                """,
                (subject_name, group_name)
            )
            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def student_courses(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Courses which studens is attending.\n
    :param conn: db connection instance.
    :return: list of affected rows.
    """
    student_name = input(">>> Enter student name: ").strip()

    with conn:

        try:
            result = conn.execute(
                """SELECT subject_name FROM
                subjects
                    INNER JOIN marks USING(subject_id)
                    INNER JOIN students USING(student_id)
                GROUP BY subject_name, student_name
                HAVING student_name = ?
                ORDER BY subject_name;
                """,
                (student_name,)
            )
            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def tutor_student_courses(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Subjects which tutor teaches student.\n
    :param conn: db connection instance.
    :return: list of affected rows.
    """
    tutor_name = input(">>> Enter tutor: ").strip()
    student_name = input(">>> Enter student: ").strip()

    with conn:

        try:
            result = conn.execute(
                """SELECT DISTINCT subject_name FROM
                tutors
                    INNER JOIN subjects USING(tutor_id)
                    INNER JOIN marks USING(subject_id)
                    INNER JOIN students USING(student_id)
                WHERE tutor_name = ? AND student_name = ?
                """,
                (tutor_name, student_name)
            )
            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def avg_tutor_student(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Average result for subjects which tutor teaches student.\n
    :param conn: db connection instance.
    :return: list of affected rows.
    """
    tutor_name = input(">>> Enter tutor: ").strip()
    student_name = input(">>> Enter student: ").strip()

    with conn:

        try:
            result = conn.execute(
                """SELECT subject_name, ROUND(AVG(result), 2) as average FROM
                tutors
                    INNER JOIN subjects USING(tutor_id)
                    INNER JOIN marks USING(subject_id)
                    INNER JOIN students USING(student_id)
                GROUP BY subject_name, student_name
                HAVING tutor_name = ? AND student_name = ?;
                """,
                (tutor_name, student_name)
            )
            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


def avg_tutor_marks(conn: sqlite3.Connection) -> tuple[tuple, list]:
    """
    Average tutor marks.\n
    :param conn: db connection instance.
    :return: list of affected rows.
    """
    tutor_name = input(">>> Enter tutor: ").strip()

    with conn:

        try:
            result = conn.execute(
                """SELECT subject_name, ROUND(AVG(result), 2) AS average FROM
                tutors
                    INNER JOIN subjects USING(tutor_id)
                    INNER JOIN marks USING(subject_id)
                GROUP BY subject_name
                HAVING tutor_name = ?;
                """,
                (tutor_name,)
            )
            return result.description, result.fetchall()

        except Exception as e:
            logging.error(e)


QUERIES = {
    "1": five_max_avg,
    "2": one_max_avg,
    "3": avg_subject_in_group,
    "4": avg_on_course,
    "5": tutor_subjects,
    "6": students_in_group,
    "7": students_marks_by_group_and_subject,
    "8": last_lesson_marks,
    "9": student_courses,
    "10": tutor_student_courses,
    "11": avg_tutor_student,
    "12": avg_tutor_marks,
}


def run():
    db_name = "hw8.db"
    db_path = BASE_DIR.joinpath(db_name)
    connection = sqlite3.Connection(db_path)

    generation = input(">>> Do you want to generate data ? [y/n]: ")
    if generation == 'y':
        db_path.unlink(missing_ok=True)
        connection = sqlite3.Connection(db_path)
        db_operations.create_database_tables(connection)
        data_generation.generate_random_db_data(connection)
    print(
        "\nEnter one following digits to obtain data:",
        "1. Will show you five students with the highest average marks.",
        "2. Will show you one student with the highest average result for desired subject.",
        "3. Will show you average result in one group for one subject.",
        "4. Will shouw you average course result.",
        "5. Will show you subjects which tutor is teaching.",
        "6. Will show you list of students in group.",
        "7. WIll show you students marks for subjects in one group.",
        "8. Will show you students marks on the last lesson for one subject.",
        "9. Will show you list of subjects which are attending by student.",
        "10. Will show you list of subjects which are being tought to student by tutor.",
        "11. Will shouw you average result which tutor is puting to student.",
        "12. Will show you average tutor marks.",
        "To break enter: X",
        sep="\n"
    )
    while True:

        action = input(">>> Enter digit or X to stop: ").strip()
        if action == "X":
            break

        operation = QUERIES.get(action)
        if operation is None:
            continue
        names, affected_rows = operation(connection)
        names = list(map(lambda x: x[0], names))
        rows_quantity = len(names)
        template = "|{:^20}|" * rows_quantity

        if affected_rows:

            print(template.format(*names))
            for row in affected_rows:
                print(template.format(*row))

        else:
            print('No such result')
