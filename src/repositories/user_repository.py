from unittest import result
from entities.user import User
from database_con import get_db_connection

class UserRepository:

    def __init__(self, conn) -> None:
        self.conn = conn
        self._cursor = self.conn.cursor()
    
    def login(self, username, password):
        self._cursor.execute("SELECT name, username, password FROM Users WHERE username=%s AND password=%s",(username, password))

        try:
            result = self._cursor.fetchone()
            return User(result[0], result[1], result[2])
        except:
            return None

    def user_exists(self, username):
        self.conn.cursor().execute("SELECT username FROM Users WHERE username=%s",(username))
        return self.conn.cursor().fetchone() != None
    
    def signup(self, user):
        self.conn.cursor().execute("INSERT INTO Users VALUES (%s, %s, %s)", (user.name, user.username, user.password))
        self.conn.commit()

        return user
        
user_repository = UserRepository(get_db_connection())