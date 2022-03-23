import database_con

conn = database_con.get_db_connection()

conn.cursor().execute("CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT, password TEXT)")
conn.commit()