class Notification:

    def __init__(self, message, title) -> None:
        self.message = message
        self.title = title

    def __str__(self):
        return f"Message: {self.message}, Title: {self.title}"
