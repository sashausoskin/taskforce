class Organization:

    def __init__(self, name, code, id=None) -> None:
        self.id = id
        self.name = name
        self.code = code
    
    def __str__(self) -> str:
        return f"Name: {self.name}, Code: {self.code}"