class Organization:

    def __init__(self, name, code, id=None) -> None:
        self.name = name
        self.code = code
        self.id = id
    
    def __str__(self) -> str:
        return f"Name: {self.name}, Code: {self.code}"