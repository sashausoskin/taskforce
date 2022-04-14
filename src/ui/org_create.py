from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from taskforce_service import OrgExists, taskforce_service, InvalidCode
from ui.messages import error, success

from ui.org_create_form_ui import Ui_CreateOrg
from ui.main_window import MainWindow


class OrgCreateForm(QDialog, Ui_CreateOrg):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        self.setupUi(self)
        self.setWindowTitle("Create organization")
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setUpConnection()

    def setUpConnection(self):
        self.buttonBox.accepted.connect(self.createOrg)

    def createOrg(self):
        try:
            if self.codeFill.text().strip() == "" or self.nameFill.text().strip() == "":
                error("Required fields empty",
                      "Please enter all the required fields!")
            else:
                self.buttonBox.accepted.disconnect()
                org = taskforce_service.create_org(
                    self.nameFill.text(), self.codeFill.text())
                success("Created organization",
                        f"You have succesfully created the organization {org.name}")
                self.close()

        except OrgExists:
            error("Code already in use",
                  "Another organization is already using this code. Please select another code!")
