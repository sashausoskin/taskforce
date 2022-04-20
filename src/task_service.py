from datetime import datetime
from entities.task import Task
from repositories.task_repository import task_repository
from user_service import user_service
from org_service import org_service


class TaskService:
    def __init__(self) -> None:
        self._task_repository = task_repository
        self._tasks = []

    def get_orgs(self):
        return user_service.get_current_user().organizations

    def get_tasks(self):
        self._tasks = self._task_repository.fetch_tasks(
            user_service.get_current_user().id,
            org_service.get_current_org().id,
            org_service.is_admin())
        return self._tasks

    def mark_as_done(self, task):
        self._task_repository.mark_as_done(task.task_id)

    def assign_task(self, assigned_to, title, desc):
        task = Task(title, desc, user_service.get_current_user(),
                    assigned_to, datetime.now())
        self._task_repository.assign_task(
            task, org_service.get_current_org().id)
        return task

    def check_notifications(self):
        return self._task_repository.check_notifications(user_service.get_current_user().id)

    def send_notification(self, user, message, title):
        self._task_repository.send_notification(
            user.id, message, title)

    def delete_tasks(self):
        self._task_repository.delete_users_tasks(
            user_service.get_current_user().id)

    def signout(self):
        self._tasks = None


task_service = TaskService()
