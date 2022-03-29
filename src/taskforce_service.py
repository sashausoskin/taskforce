from PyQt5.QtWidgets import QErrorMessage
from entities.user import User
from repositories.user_repository import user_repository
from repositories.org_repository import org_repository

class UsernameExists(Exception):
    pass

class WrongCredentials(Exception):
    pass

class InvalidCode(Exception):
    pass

class OrgExists(Exception):
    pass

class TaskforceService:
    def __init__(self) -> None:
        self._user_repository = user_repository
        self._org_repository = org_repository
    
    def login(self, username, password):

        user = self._user_repository.login(username, password)

        if not user:
            raise WrongCredentials()
        
        self._user=user
        return user



    def signup(self, name, username, password):

        if self._user_repository.user_exists(username):
            raise UsernameExists()
        
        self._user = self._user_repository.signup(User(name, username, password))
        return self._user
    
    def get_username(self):
        return self._user.username
    
    def delete_user(self, username):
        self._user_repository.delete_user(username)
    
    def join_org(self, code):
        org = self._org_repository.fetch_org(code)
        if not org:
            raise InvalidCode
        
        self._org_repository.add_to_org(self._user.id, org.id)
        self._user.organizations.append(org)
        return org
    
    def create_org(self, name, code):
        if self._org_repository.fetch_org(code):
            raise OrgExists
        
        return self._org_repository.create_org(name, code, self._user.id)


taskforce_service = TaskforceService()