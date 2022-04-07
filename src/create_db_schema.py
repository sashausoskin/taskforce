from psycopg2.errors import DuplicateTable
import database_con

conn = database_con.get_db_connection()

commands=[
    "CREATE TABLE Users (id SERIAL PRIMARY KEY, name TEXT, username TEXT, password TEXT);",
    "CREATE TABLE Organizations (id SERIAL PRIMARY KEY, name TEXT, code TEXT);",
    """CREATE TABLE OrgMembers
        (member INTEGER REFERENCES Users, org INTEGER REFERENCES Organizations, admin BOOLEAN);""",
    """CREATE TABLE Tasks
        (id SERIAL PRIMARY KEY, title TEXT, description TEXT, assigned_by INTEGER REFERENCES Users, assigned_to INTEGER REFERENCES Users, org INTEGER REFERENCES Organizations, done BOOLEAN);"""
]

for command in commands:
    try:
        conn.cursor().execute(command)
    except DuplicateTable:
        conn.commit()

conn.commit()

