class User:

    def __init__(self, name, username, password, user_id=None) -> None:
        self.id = user_id
        self.name = name
        self.username = username
        self.password = password
        self.organizations = []

    def __str__(self) -> str:
        return f"Name: {self.name}, Username: {self.username}"
