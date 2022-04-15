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

    def login(self, username, password):

        user = self._user_repository.login(username, password)

        if not user:
            raise WrongCredentials()

        user.organizations = self._org_repository.org_member(user.id)
        self._user = user
        return user

    def signup(self, name, username, password):

        if self._user_repository.user_exists(username):
            raise UsernameExists()

        self._user = self._user_repository.signup(
            User(name, username, password))
        return self._user

    def delete_user(self, username):
        self._user_repository.delete_user(username)

    def signout(self):
        self._user = None

    def get_current_user(self):
        return self._user


user_service = UserService()
