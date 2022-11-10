import logging


def create_database_tables(conn) -> None:
    """
    Creating tables according to ER-diagram in readme.
    :return: None
    """
    with open('schemas.sql', 'r') as f:
        sql = f.read()

    with conn:
        try:
            conn.executescript(sql)
        except Exception as e:
            logging.error(e)


def insert_into_table(conn, query: str, data: list) -> None:
    with conn:

        try:
            conn.executemany(query, data)
        except Exception as e:
            logging.error(e)


def select_from_table(conn, query: str) -> list:
    with conn:

        try:
            result = conn.execute(query)
            return result.fetchall()

        except Exception as e:
            logging.error(e)
