
class Task:

    def __init__(self, title, description,
                 assigned_by, assigned_to,
                 assigned_on, task_id=None, done_on=None) -> None:
        self.title = title
        self.desc = description
        self.assigned_by = assigned_by
        self.assigned_to = assigned_to
        self.task_id = task_id
        self.assigned_on = assigned_on
        self.done_on = done_on

    def __str__(self) -> str:
        return f"""Title: {self.title},
            Desc: {self.desc},
            Assigned_by:({self.assigned_by}),
            Assigned_to:({self.assigned_to}),
            Done on: ({self.done_on})"""
