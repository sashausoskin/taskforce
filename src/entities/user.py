class User:

    def __init__(self, name, username, password) -> None:
        self.name = name
        self.username = username
        self.password = password
    
    def __str__(self) -> str:
        return f"Name: {self.name}, Username: {self.username}, Password:{self.password}"