import database_con

conn = database_con.get_db_connection()

try:
    conn.cursor().execute("DROP TABLE Users;")
    conn.commit()
except:
    conn.commit()

conn.cursor().execute("CREATE TABLE Users (id SERIAL PRIMARY KEY, name TEXT, username TEXT, password TEXT)")
conn.cursor().execute("INSERT INTO Users (name, username, password) VALUES ('Testy McTester', 'test1', '1234');")
conn.commit()