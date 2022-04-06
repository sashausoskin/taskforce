from entities.task import Task
from entities.user import User
from database_con import get_db_connection

class TaskRepository:

    def __init__(self, conn) -> None:
        self.conn = conn
        self._cursor = self.conn.cursor()

    def fetch_tasks(self, user_id, admin):
        if not admin:
            self._cursor.execute("""SELECT T.title, T.description, T.id, T.done, U_by.name, U_By.username, U_By.id, U_To.name, U_To.username, U_To.id 
                FROM Tasks T LEFT JOIN Users U_To ON T.assigned_to = U_To.id LEFT JOIN Users U_By ON T.assigned_by = U_By.id 
                WHERE T.assigned_to = %s ORDER BY T.id;""", (user_id, ))
        results = self._cursor.fetchall()
        task_list = []
        for result in results: 
            assigned_by_user = User(result[4], result[5], "", result[6])
            assigned_to_user = User(result[7], result[8], "", result[9])
            task_list.append(Task(result[0], result[1], assigned_by_user, assigned_to_user, result[2], result[3]))
        
        return task_list

    def mark_as_done(self, task_id):
        self._cursor.execute("UPDATE Tasks SET done=TRUE WHERE id=%s", (task_id, ))
        self.conn.commit()

task_repository = TaskRepository(get_db_connection())