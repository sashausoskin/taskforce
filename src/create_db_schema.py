from psycopg2.errors import DuplicateTable  # pylint: disable=no-name-in-module
# Pylint is disabled above because of a false positive.
# Pylint says that there is no DuplicateTable member in psycopg2.errors,
# even though the program runs without problems.
import database_con

conn = database_con.get_db_connection()

commands = [
    """CREATE TABLE Users
        (id SERIAL PRIMARY KEY,
        name TEXT,
        username TEXT,
        password TEXT);""",
    """CREATE TABLE Organizations
        (id SERIAL PRIMARY KEY,
        name TEXT,
        code TEXT);""",
    """CREATE TABLE OrgMembers
        (member INTEGER REFERENCES Users,
        org INTEGER REFERENCES Organizations,
        admin BOOLEAN);""",
    """CREATE TABLE Tasks
        (id SERIAL PRIMARY KEY,
        title TEXT,
        description TEXT,
        assigned_by INTEGER REFERENCES Users,
        assigned_to INTEGER REFERENCES Users,
        org INTEGER REFERENCES Organizations,
        done BOOLEAN,
        assigned_on TIMESTAMP,
        done_on TIMESTAMP);""",
    """CREATE TABLE Notifications
        (user_id INTEGER REFERENCES Users,
        message TEXT,
        title TEXT);"""
]

for command in commands:
    try:
        conn.cursor().execute(command)
        conn.commit()
    except DuplicateTable:
        conn.commit()

conn.commit()
