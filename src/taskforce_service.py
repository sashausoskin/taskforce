from entities.user import User
from entities.task import Task
from repositories.user_repository import user_repository
from repositories.org_repository import org_repository
from repositories.task_repository import task_repository


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
        self._user = None
        self._org = None
        self._user_repository = user_repository
        self._org_repository = org_repository
        self._task_repository = task_repository
        self._tasks = []

    def login(self, username, password):

        user = self._user_repository.login(username, password)

        if not user:
            raise WrongCredentials()

        user.organizations = self._org_repository.org_member(user.id)
        self._user = user
        if len(user.organizations) > 0:
            self._org = user.organizations[0]
        return user

    def signup(self, name, username, password):

        if self._user_repository.user_exists(username):
            raise UsernameExists()

        self._user = self._user_repository.signup(
            User(name, username, password))
        return self._user

    def get_username(self):
        return self._user.username

    def get_all_members_in_org(self):
        return self._org_repository.get_members(self._org.id)

    def get_name(self):
        return self._user.name

    def get_orgs(self):
        return self._user.organizations

    def delete_user(self, username):
        self._user_repository.delete_user(username)

    def join_org(self, code):
        org = self._org_repository.fetch_org(code)
        if not org:
            raise InvalidCode

        self._org_repository.add_to_org(self._user.id, org.id)
        self._user.organizations.append(org)
        self._org = org
        return org

    def create_org(self, name, code):
        if self._org_repository.fetch_org(code):
            raise OrgExists

        org = self._org_repository.create_org(name, code, self._user.id)
        self._user.organizations.append(org)
        self._org = org
        return org

    def delete_org(self, org_id):
        self._org_repository.delete_org(org_id)

    def get_tasks(self):
        self._tasks = self._task_repository.fetch_tasks(
            self._user.id, self.is_admin())
        return self._tasks

    def get_task_by_id(self, task_id):
        for task in self._tasks:  # This could be optimized
            if task.task_id == task_id:
                return task
        return None

    def mark_as_done(self, task):
        self._task_repository.mark_as_done(task.task_id)

    def is_admin(self):
        return self._org_repository.is_admin(self._org.id, self._user.id)

    def assign_task(self, assigned_to, title, desc):
        task = Task(title, desc, self._user, assigned_to)
        self._task_repository.assign_task(task, self._org.id)
        return task

    def check_notifications(self):
        return self._task_repository.check_notifications(self._user.id)

    def send_notification(self, user, message, notification_type):
        self._task_repository.send_notification(
            user.id, message, notification_type)

    def delete_tasks(self):
        self._task_repository.delete_users_tasks(self._user.id)

    def signout(self):
        self._user = None
        self._org = None
        self._tasks = []


taskforce_service = TaskforceService()
