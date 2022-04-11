from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox
from PyQt5.QtGui import QIcon
from taskforce_service import taskforce_service, InvalidCode
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
                org = taskforce_service.join_org(self.codeFill.text())
                success("Joined organizations",
                        f"You have succesfully joined the organization {org.name}")
                self.openMainWindow()

        except InvalidCode:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("message")
            msg.setWindowTitle("title")
            msg.exec_()

    def createOrg(self):
        self.org_create_form.buttonBox.accepted.connect(self.openMainWindow)
        self.org_create_form.exec()

    def openMainWindow(self):
        print("Opening main window")
        self._win = MainWindow()
        self._win.show()
        self.close()
