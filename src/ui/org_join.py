from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from user_service import user_service
from org_service import org_service, InvalidCode
from ui.messages import error, success
import plyer

from ui.org_join_window_ui import Ui_OrgJoin
from ui.org_create import OrgCreateForm
from ui.main_window import MainWindow


class OrgJoinWindow(QMainWindow, Ui_OrgJoin):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("TaskForce")
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setUpConnection()
        self.org_create_form = OrgCreateForm(self)

    def setUpConnection(self):
        self.joinButton.pressed.connect(self.joinOrg)
        self.createButton.pressed.connect(self.createOrg)

    def joinOrg(self):

        try:
            if self.codeFill.text().strip() == "":
                error("Required fields empty",
                      "Please enter the code for the organization you want to join.")
            else:
                org = org_service.join_org(self.codeFill.text())
                success("Joined organizations",
                        f"You have succesfully joined the organization {org.name}")
                self.openMainWindow()

        except InvalidCode:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Organization not found!")
            msg.setWindowTitle("There is no organiozation with this code. Make sure that you wrote the code correctly.")
            msg.exec_()

    def createOrg(self):
        self.org_create_form.exec()

    def openMainWindow(self):
        self.joinButton.disconnect()
        self._win = MainWindow()
        self._win.show()
        self.close()
