from PyQt5.QtWidgets import QMessageBox, QDialog
from taskforce_service import taskforce_service, UsernameExists
from ui.org_join import OrgJoinWindow

from ui.signup_form_ui import Ui_signupDialog


class SignupForm(QDialog, Ui_signupDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()
        self.setWindowTitle("Sign up")
        self.parent = parent

    def connectSignalSlots(self):
        self.buttonBox.accepted.connect(self.signup)

    def signup(self):
        if self.nameFill.text().strip() == "" or self.usernameFill.text().strip() == "" or self.passwordFill.text().strip() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please enter all the required fields!")
            msg.setWindowTitle("Error")
            msg.exec_()

        else:
            try:
                user = taskforce_service.signup(self.nameFill.text(
                ), self.usernameFill.text(), self.passwordFill.text())
                taskforce_service.login(user.username, user.password)

                self.win = OrgJoinWindow()
                self.hide()
                self.parent.close()
                self.win.org_create_form.buttonBox.accepted.connect(self.win.openMainWindow)
                self.win.show()

            except UsernameExists:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(
                    "The username or name is already taken. Please try again!")
                msg.setWindowTitle("Error")
                msg.exec_()
