import bcrypt
from entities.user import User
from database_con import get_db_connection


class UserRepository:

    def __init__(self, conn) -> None:
        self.conn = conn
        self._cursor = self.conn.cursor()

    def login(self, username, password):
        """Retrieves a user from the database whose credentials math the given ones

        Args:
            username (string): The username with which the user is trying to log in
            password (string): The password with which the user is trying to log in

        Returns:
            User:   Returns a User object if a user matching the username
                    and password is found from the database

            None:   If the user is not found, return None
        """
        if username == "" or password == "":
            return None

        self._cursor.execute(
            "SELECT name, username, password, id FROM Users WHERE username=%s;",
            (username, ))

        try:
            result = self._cursor.fetchone()
            if not bcrypt.checkpw(password.encode("utf-8"), result[2].encode("utf-8")):
                return None
            return User(result[0], result[1], result[2], result[3])
        except TypeError:
            return None

    def user_exists(self, username: str):
        """Checks if a username already exists in a database

        Args:
            username (str): The username that will be checked

        Returns:
            True: If the username is already in the database
            False: If otherwise
        """
        self._cursor.execute(
            "SELECT username FROM Users WHERE username=%s;", (username, ))

        return self._cursor.fetchone() is not None

    def signup(self, user: User):
        """Adds a user to the database

        Args:
            user (User): The user that will be added to the database

        Returns:
            User: A User-object that was added to the database
            with the additional ID value that was generated when the user was added to the database
        """
        pwd_encode = user.password.encode("utf-8")
        salt = bcrypt.gensalt()

        self._cursor.execute("INSERT INTO Users (name, username, password) VALUES (%s, %s, %s);",
                             (user.name, user.username,
                             bcrypt.hashpw(pwd_encode, salt).decode("utf-8")))
        self.conn.commit()

        return self.login(user.username, user.password)

    def delete_user(self, username):
        """Deletes a user from the database. Mainly used for testing purposes.

        Args:
            username (string): The username of the user whose account will be deleted
        """
        self._cursor.execute(
            "DELETE FROM Users where username=%s;", (username,))
        self.conn.commit()


user_repository = UserRepository(get_db_connection())
