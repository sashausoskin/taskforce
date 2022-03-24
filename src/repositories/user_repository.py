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
        self._cursor.execute("SELECT username FROM Users WHERE username=%s;",(username,))

        return self._cursor.fetchone() != None
    
    def signup(self, user):
        self._cursor.execute("INSERT INTO Users (name, username, password) VALUES (%s, %s, %s)", (user.name, user.username, user.password))
        self.conn.commit()

        return user
        
user_repository = UserRepository(get_db_connection())