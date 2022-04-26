from datetime import datetime
import psycopg2.extras
from entities.notification import Notification
from entities.task import Task
from entities.user import User
from entities.comment import Comment
from database_con import get_db_connection


class TaskRepository:

    def __init__(self, conn, bg_conn) -> None:
        self.conn = conn
        self._cursor = self.conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

        self.bg_conn = bg_conn
        self._bg_cursor = self.bg_conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

    def fetch_tasks(self, user_id: int, org_id: int, admin: bool, filters: list):
        """Retrieves all of the user's tasks in an organisation from the database

        Args:
            user_id (integer):  ID of the users whose tasks are going to be retrieved
            org_id (integer):   ID of the organisations where the tasks are
            admin (bool):       Is the query done as an admin or not
            filters ([str]):    A list of filters that are used in the query.

        Returns:
            [Task]: A list of Task objects that are assigned to the user if they are not an admin.
                    Otherwise a list of tasks that were given out in the organisation
        """

        query_filters = ""

        if filters is not None:
            if "user_assigned" in filters:
                # Potential for injection?
                query_filters += f"AND T.assigned_by = {user_id}"
            if "undone" in filters:
                query_filters += "AND T.done_on IS NULL"

        if not admin:
            self._cursor.execute("""SELECT T.title, T.description, T.id, T.assigned_on, T.done_on,
                U_by.name, U_By.username, U_By.id, U_To.name, U_To.username, U_To.id
                FROM Tasks T LEFT JOIN Users U_To ON T.assigned_to = U_To.id LEFT JOIN Users U_By ON T.assigned_by = U_By.id 
                WHERE T.assigned_to = %s AND org = %s ORDER BY T.id;""", (user_id, org_id))
        else:
            self._cursor.execute(f"""SELECT T.title, T.description, T.id, T.assigned_on, T.done_on,
                U_by.name, U_By.username, U_By.id, U_To.name, U_To.username, U_To.id
                FROM Tasks T LEFT JOIN Users U_To ON T.assigned_to = U_To.id LEFT JOIN Users U_By ON T.assigned_by = U_By.id 
                WHERE org = %s {query_filters} ORDER BY T.id;""", (org_id, ))

        results = self._cursor.fetchall()
        task_list = []
        for result in results:
            assigned_by_user = User(result[5], result[6], "", result[7])
            assigned_to_user = User(result[8], result[9], "", result[10])
            task_list.append(Task(
                result[0], result[1], assigned_by_user,
                assigned_to_user, result[3], result[2], result[4]))

        return task_list

    def mark_as_done(self, task_id: int):
        """Marks a task as done in the database

        Args:
            task_id (int):  ID of the task that is going to be marked as done
                            and given a completion time.
        """
        self._cursor.execute(
            "UPDATE Tasks SET done_on=%s WHERE id=%s;", (datetime.now(), task_id))
        self.conn.commit()

    def assign_task(self, task: Task, org_id: int):
        """Adds a task to the database

        Args:
            task (Task):        The task that is going to be added to the database
            org_id (integer):   The ID of the organisation where the task was assigned
        """
        self._cursor.execute("""INSERT INTO Tasks
                                (title, description, assigned_by, assigned_to, org, assigned_on)
                                VALUES (%s, %s, %s, %s, %s, %s);""",
                             (task.title, task.desc, task.assigned_by.id,
                              task.assigned_to.id, org_id, task.assigned_on))
        self.conn.commit()

    def check_notifications(self, user_id: int):
        """ Checks if a user has received any notifications,
            and if has, deletes them from the database

        Args:
            user_id (integer):  The ID of the user whose notifications you want to check and delete

        Returns:
            [Notification]:     A list of Notification-objects that were sent to the user
        """

        self._bg_cursor.execute(
            "SELECT message, title FROM Notifications WHERE user_id=%s;", (user_id, ))

        notifications = []

        for result in self._bg_cursor.fetchall():
            notifications.append(Notification(result[0], result[1]))

        self._bg_cursor.execute(
            "DELETE FROM Notifications WHERE user_id=%s;", (user_id, ))
        self.bg_conn.commit()

        return notifications

    def send_notification(self, user_id: int, message: str, title: str):
        """Adds a notification to the database to be sent.

        Args:
            user_id (integer):  ID of the user to whom the notification will be sent
            message (string):   The main message of the notification
            title (string):     The header/title of the notification
        """
        self._cursor.execute(
            "INSERT INTO Notifications VALUES (%s, %s, %s);", (user_id, message, title))
        self.conn.commit()

    def delete_users_tasks(self, user_id : int):
        """ Deletes all of the tasks that were assigned to a user from the database.
            Mainly used for testing purposes.

        Args:
            user_id (integer): ID of the users whose tasks are going to be deleted.
        """
        self._cursor.execute(
            "DELETE FROM Tasks WHERE assigned_to=%s;", (user_id, )
        )
        self.conn.commit()

    def get_comments(self, org_id: int):
        """Gets all of the comments posted in an organisation.

        Args:
            org_id (integer):   ID of the organisation from which the comments will be retrieved.

        Returns:
            {[Comment]}:        A dictionary, where the key is the ID of the task
                                under which the comments were posted
                                and the value is a list of Comment-objects.
        """

        self._cursor.execute(
            """SELECT C.id, C.task_id, C.message, C.time,
                U.id, U.name, U.username
                FROM Comments C LEFT JOIN Users U ON C.sent_by=U.id
                LEFT JOIN Tasks T ON C.task_id = T.id WHERE T.org = %s;""",
                (org_id, )
        )

        results = self._cursor.fetchall()

        comments = {}

        for result in results:
            comments[result[1]] = []

        for result in results:
            comments[result[1]].append(Comment(result[1], result[2], result[3], User(
                result[5], result[6], "", result[4]), result[0]))

        return comments

    def post_comment(self, task_id: int, message: str, sent_by_user_id: int):
        """Adds a new comment to the database

        Args:
            task_id (integer):          The ID of the task under which the comment will be added.
            message (string):           The contents of the comment
            sent_by_user_id (integer):  The ID of user who sent the comment
        """
        self._cursor.execute(
            "INSERT INTO Comments (task_id, message, time, sent_by) VALUES (%s, %s, %s, %s);", (
                task_id, message, datetime.now(), sent_by_user_id)
        )

        self.conn.commit()

    def delete_users_comments(self, user_id : int):
        """Deletes all of the comments posted by a user. Mainly used for testing purposes

        Args:
            user_id (int): The ID of the users whose comments will be deleted
        """
        self._cursor.execute("DELETE FROM Comments WHERE sent_by=%s", (user_id, ))

task_repository = TaskRepository(get_db_connection(), get_db_connection())
