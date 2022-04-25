from entities.user import User

class Comment:

    def __init__(self, task_id, message, date, sent_by : User, comment_id = None) -> None:
        self.id = comment_id
        self.task_id = task_id
        self.message = message
        self.date = date
        self.sent_by = sent_by

    def __str__(self) -> str:
        return f"Message: {self.message}, Sent by: {self.sent_by.username}"