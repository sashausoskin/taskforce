from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from services.org_service import org_service
from services.task_service import task_service
from ui.messages import error

from ui.new_task_form_ui import Ui_NewFormDialog


class NewTaskForm(QDialog, Ui_NewFormDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        self.setupUi(self)
        self.setWindowTitle("New task")
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setUpConnection()

        self.members = org_service.get_all_members_in_org()
        if len(self.members)==0:
            self.buttonBox.setEnabled(False)

        for member in self.members:
            self.assignComboBox.addItem(f"{member.name} ({member.username})")

    def setUpConnection(self):
        self.buttonBox.accepted.connect(self.assignTask)

    def assignTask(self):
        if self.taskFill.text().strip() == "" or self.descFill.toPlainText().strip() == "":
            error("Missing information", "Please enter all the required fields!")
            return

        task = task_service.assign_task(
            self.members[self.assignComboBox.currentIndex()], self.taskFill.text(), self.descFill.toPlainText())
        task_service.send_notification(
            task.assigned_to, f"A new task is available: {task.title}", "New task")
        self._parent.updateTasks()
        self.hide()
