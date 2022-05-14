import config
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from services.user_service import user_service, WrongCredentials
from services.org_service import org_service

from ui.login_window_ui import Ui_LoginScreen
from ui.signup_form import SignupForm
from ui.org_join import OrgJoinWindow
from ui.main_window import MainWindow

from ui.messages import error


class loginWindow(QMainWindow, Ui_LoginScreen):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()
        self.setWindowTitle("TaskForce")
        self.setWindowIcon(QIcon("img/icon.ico"))

        self.taskforceLogo.setPixmap(
            QPixmap("img/icon.png"))  # Change the icon to a relative path

    def connectSignalSlots(self):
        self.loginButton.pressed.connect(self.login)
        self.signupButton.pressed.connect(self.signupForm)

    def login(self):
        try:
            if self.usernameFill.text().strip() == "" or self.passwordFill.text().strip() == "":
                error("Error", "Please fill all the required fields!")
            else:
                user = user_service.login(
                    self.usernameFill.text(), self.passwordFill.text())

                if self.autoLoginCheck.isChecked():
                    config.get_config()[
                        "AUTO_LOGIN"]["username"] = self.usernameFill.text().strip()
                    config.get_config()[
                        "AUTO_LOGIN"]["password"] = self.passwordFill.text().strip()
                    config.save_changes()
                if len(user.organizations) == 0:
                    self._win = OrgJoinWindow()
                    self._win.org_create_form.buttonBox.accepted.connect(
                        self.openMainWindow)
                    self.hide()
                    self._win.show()
                else:
                    org_service.set_current_org(user.organizations[0], False)
                    try:
                        for org in user.organizations:  # Set the selected org as the one which the user selected in the previous session
                            if org.id == int(config.config["AUTO_LOGIN"]["SELECTED_ORG"]):
                                org_service.set_current_org(org)
                    except:
                        pass
                    self.loginButton.disconnect()
                    self._win = MainWindow()
                    self.hide()
                    self._win.show()

        except WrongCredentials:
            error("User not found",
                  "The username couldn't be found or the password is incorrect. Please try again!")

    def signupForm(self):
        self._win = SignupForm(self)
        self._win.exec()

    def openMainWindow(self):
        if self._win.org_create_form.error == False:
            self._win.openMainWindow()
