import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox
from PyQt5.QtGui import QIcon
from taskforce_service import taskforce_service
import plyer

from ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("TaskForce")
        self.setWindowIcon(QIcon("img/check-svgrepo-com.svg"))
        self.nameLabel.setText(f"{taskforce_service.get_name()}")
        self.orgLabel.setText(taskforce_service.get_orgs()[0].name)
