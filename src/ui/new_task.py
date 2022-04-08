from PyQt5.QtWidgets import  QDialog
from PyQt5.QtGui import QIcon
from taskforce_service import OrgExists, taskforce_service, InvalidCode
from ui.messages import error, success

from ui.new_task_form_ui import Ui_NewFormDialog


class NewTaskForm(QDialog, Ui_NewFormDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        self.setupUi(self)
        self.setWindowTitle("New task")
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setUpConnection()

        for member in taskforce_service.get_all_members_in_org():
            self.assignComboBox.addItem(member.name)

    def setUpConnection(self):
        self.buttonBox.accepted.connect(self.assignTask)

    def assignTask(self):
        if self.taskFill.text().strip()=="" or self.descFill.toPlainText().strip()=="":
            error("Missing information", "Please enter all the required fields!")
            return
        
        assigned_to = taskforce_service.get_user_by_name(self.assignComboBox.currentText())
        task = taskforce_service.assign_task(assigned_to, self.taskFill.text(), self.descFill.toPlainText())
        taskforce_service.send_notification(task.assigned_to, f"A new task is available: {task.title}", "new")
        self._parent.updateTasks()
        self.hide()

