from entities.user import User
from repositories.user_repository import user_repository
from repositories.org_repository import org_repository


class UsernameExists(Exception):
    pass


class WrongCredentials(Exception):
    pass


class UserService:
    def __init__(self) -> None:
        self._user = None
        self._user_repository = user_repository
        self._org_repository = org_repository

    def login(self, username: str, password: str) -> User:
        """Tries to log the user in with the given credentials

        Args:
            username (str): The username used to log in
            password (str): The password used to log in

        Raises:
            WrongCredentials: Raised if a user matching the credentials could not be found

        Returns:
            User: Returns the User object matching the credentials
        """

        user = self._user_repository.login(username, password)

        if not user:
            raise WrongCredentials()

        user.organizations = self._org_repository.org_member(user.id)
        self._user = user
        return user

    def signup(self, name: str, username: str, password: str) -> User:
        """Creates a new user using the given credentials

        Args:
            name (str): The name of the user
            username (str): The username of the user
            password (str): The password of the user

        Raises:
            UsernameExists: Raised if a user with the given username already exists.

        Returns:
            User: Returns the newly created user as a User object with the generated ID parameter.
        """

        if self._user_repository.user_exists(username):
            raise UsernameExists()

        self._user = self._user_repository.signup(
            User(name, username, password))
        return self._user

    def delete_user(self, username: str):
        """Deletes a user's account. Mainly used for testing

        Args:
            username (str): The username of the user whose account will be deleted.
        """
        self._user_repository.delete_user(username)

    def signout(self):
        """Signs the current user out. Nullifies the current user.
        """
        self._user = None

    def get_current_user(self) -> User:
        """
        Returns:
            User: The currently logged in user.
        """
        return self._user


user_service = UserService()
