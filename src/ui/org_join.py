from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox
from PyQt5.QtGui import QIcon
from taskforce_service import taskforce_service, InvalidCode
from ui.messages import error, success
import plyer

from ui.org_join_window_ui import Ui_OrgJoin
from ui.org_create import OrgCreateForm


class OrgJoinWindow(QMainWindow, Ui_OrgJoin):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("TaskForce")
        self.setWindowIcon(QIcon("img/check-svgrepo-com.svg"))
        self.setUpConnection()
    
    def setUpConnection(self):
        self.joinButton.pressed.connect(self.joinOrg)
        self.createButton.pressed.connect(self.createOrg)
    
    def joinOrg(self):
        
        try:
            if self.codeFill.text().strip()=="":
                error("Required fields empty", "Please enter the code for the organization you want to join.")
            else:
                org = taskforce_service.join_org(self.codeFill.text())
                success("Joined organizations", f"You have succesfully joined the organization {org.name}")
                self.hide()
            
        except InvalidCode:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("message")
            msg.setWindowTitle("title")
            msg.exec_()

    def createOrg(self):
        self._form = OrgCreateForm(self)
        self._form.exec()
