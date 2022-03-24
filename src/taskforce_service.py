from PyQt5.QtWidgets import QErrorMessage
from entities.user import User
from repositories.user_repository import user_repository

class UsernameExists(Exception):
    pass

class WrongCredentials(Exception):
    pass

class TaskforceService:
    def __init__(self) -> None:
        self._user_repository = user_repository
    
    def login(self, username, password):

        user = self._user_repository.login(username, password)

        if not user:
            raise WrongCredentials()
        
        self._user=user
        return user



    def signup(self, name, username, password):

        if self._user_repository.user_exists(username):
            raise UsernameExists()
        
        self._user = self.user_repository.signup(User(name, username, password))

taskforce_service = TaskforceService()