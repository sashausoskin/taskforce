import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox
from PyQt5.QtGui import QIcon
from taskforce_service import taskforce_service, WrongCredentials
import plyer

from ui.login_window_ui import Ui_LoginScreen
from ui.signup_form import SignupForm
from ui.org_join import OrgJoinWindow
from ui.main_window import MainWindow


class loginWindow(QMainWindow, Ui_LoginScreen):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()
        self.setWindowTitle("TaskForce")
        self.setWindowIcon(QIcon("img/check-svgrepo-com.svg"))

    def connectSignalSlots(self):
        self.loginButton.pressed.connect(self.login)
        self.signupButton.pressed.connect(self.signupForm)

    def login(self):
        try:
            if self.usernameFill.text().strip() == "" or self.passwordFill.text().strip() == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Please fill all the required fields!")
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                user = taskforce_service.login(
                    self.usernameFill.text(), self.passwordFill.text())
                plyer.notification.notify(
                    title="Logged in", message=f"Welcome {user.name}")

                if len(user.organizations) == 0:
                    self._win = OrgJoinWindow()
                    self.hide()
                    self._win.show()
                else:
                    self._win = MainWindow()
                    self.hide()
                    self._win.show()

        except WrongCredentials:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(
                "The username couldn't be found or the password is incorrect. Please try again!")
            msg.setWindowTitle("User not found")
            msg.exec_()

    def signupForm(self):
        self._win = SignupForm(self)
        self._win.exec()
