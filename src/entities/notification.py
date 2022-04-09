class Notification:

    def __init__(self, message, notification_type) -> None:
        self.message = message
        self.type = notification_type

    def __str__(self):
        return f"Message: {self.message}, Type: {self.type}"
