import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import plyer

from login_window_ui import Ui_LoginScreen

class loginWindow(QMainWindow, Ui_LoginScreen):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()
        self.setWindowTitle("TaskForce")
        self.setWindowIcon(QIcon("img/check-svgrepo-com.svg"))

    
    def connectSignalSlots(self):
        self.loginButton.released.connect(self.login)
        self.signupButton.released.connect(self.signup)

    def login(self):
        print(f"Logging in as {self.usernameFill.text()}")
        plyer.notification.notify(title="Logged in", message=f"Welcome {self.usernameFill.text()}")
    
    def signup(self):
        print("Signing up")

def draw_loginWindow():
    app = QApplication(sys.argv)
    win = loginWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    draw_loginWindow()