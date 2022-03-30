from sqlite3 import ProgrammingError
import database_con

conn = database_con.get_db_connection()

try:
    conn.cursor().execute("DROP TABLE OrgMembers;")
    conn.cursor().execute("DROP TABLE Users;")
    conn.cursor().execute("DROP TABLE Organizations;")
    conn.commit()
except ProgrammingError:
    conn.commit()

conn.cursor().execute(
    "CREATE TABLE Users (id SERIAL PRIMARY KEY, name TEXT, username TEXT, password TEXT)")
conn.cursor().execute(
    "CREATE TABLE Organizations (id SERIAL PRIMARY KEY, name TEXT, code TEXT);")
conn.cursor().execute(
    """CREATE TABLE OrgMembers
    (member INTEGER REFERENCES Users, org INTEGER REFERENCES Organizations, admin BOOLEAN);""")
conn.commit()
