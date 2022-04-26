from datetime import datetime
from entities.comment import Comment
from entities.organization import Organization
from entities.task import Task
from entities.user import User
from entities.notification import Notification
from repositories.task_repository import task_repository
from services.user_service import user_service
from services.org_service import org_service


class TaskService:
    def __init__(self) -> None:
        self._task_repository = task_repository
        self._tasks = []
        self._comments = {}

    def get_tasks(self, filters: list = None) -> list:
        """Gets all of the tasks assigned to the current user,
            or if the user is an admin, then fetches all of the tasks of the organizations

        Args:
            filters ([str], optional):  How the query should be limited. Defaults to None.
                Can use the following keywords:
                "undone": Only show tasks that have not been finished.
                "user_assigned":    Only show the tasks assigned
                                    by the current user.

        Returns:
            [Task]: A list of Task objects.
        """
        self._tasks = self._task_repository.fetch_tasks(
            user_service.get_current_user().id,
            org_service.get_current_org().id,
            org_service.is_admin(),
            filters)
        return self._tasks

    def mark_as_done(self, task: Task):
        """Marks a task as done

        Args:
            task (Task): The task that will be marked as done.
        """
        self._task_repository.mark_as_done(task.id)

    def assign_task(self, assigned_to: User, title: str, desc: str) -> Task:
        """Assigns a task to a user

        Args:
            assigned_to (User): The user to whom the task will be assigned
            title (str): The header of the task
            desc (str): The description of the task

        Returns:
            Task: The newly assigned task as a Task object
        """
        task = Task(title, desc, user_service.get_current_user(),
                    assigned_to, datetime.now())
        self._task_repository.assign_task(
            task, org_service.get_current_org().id)
        return task

    def check_notifications(self) -> list:
        """Checks if the current user has received any notifications

        Returns:
            [Notification]: A list of notifications the user has received
        """
        return self._task_repository.check_notifications(user_service.get_current_user().id)

    def send_notification(self, user: User, message: str, title: str):
        """Sends a notification to a user

        Args:
            user (User): The user to whom the notification will be sent
            message (str): The contents of the notification
            title (str): The header of the notification
        """
        self._task_repository.send_notification(
            user.id, message, title)

    def delete_tasks(self):
        """Deletes all of the tasks assigned to the current user. Mainly used for testing purposes.
        """
        self._task_repository.delete_users_tasks(
            user_service.get_current_user().id)

    def update_comments_in_memory(self):
        """Fetches all of the comments in the current organization and saves them in memory.
        """
        self._comments = self._task_repository.get_comments(
            org_service.get_current_org().id)

    def get_comments_from_memory(self) -> dict:
        """Fetches all of the comments saved into memory.

        Returns:
            {Comment}:  Returns a dictionary where the key is the task
                        under which the comment was posted
                        and value is a list of Comment objects
        """
        return self._comments

    def post_comment(self, task: Task, message: str):
        """Posts a new comment

        Args:
            task (Task): The Task under which the comment will be posted
            message (str): The contents of the comment
        """
        self._task_repository.post_comment(
            task.id, message, user_service.get_current_user().id)

        if task.id not in self._comments:
            self._comments[task.id] = [
                Comment(task.id, message, datetime.now(), user_service.get_current_user())]
        else:
            self._comments[task.id].append(
                Comment(task.id, message, datetime.now(), user_service.get_current_user()))
    
    def delete_users_comments(self, user : User):
        """Deletes all of the comments posted by a user. Mainly used for testing purposes

        Args:
            user (User): The user whose comments will be deleted
        """
        self._task_repository.delete_users_comments(user.id)

    def signout(self):
        """Used when signing out. Nullifies the currently active organization.
        """
        self._tasks = None


task_service = TaskService()
