from functools import partial
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon
from taskforce_service import taskforce_service
import plyer

from ui.main_window_ui import Ui_MainWindow
from ui.new_task import NewTaskForm


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent=parent
        self.setupUi(self)
        self.setWindowTitle("TaskForce")
        self.setWindowIcon(QIcon("img/check-svgrepo-com.svg"))
        self.isAdmin = taskforce_service.is_admin()
        self.nameLabel.setText(f"{taskforce_service.get_name()}")
        if self.isAdmin:
            self.orgLabel.setText(f"{taskforce_service.get_orgs()[0].name} (Admin)")
        else:
            self.orgLabel.setText(f"{taskforce_service.get_orgs()[0].name} (Member)")
        self.selectedTaskButton = None
        self.actionSign_out.triggered.connect(self.signOut)
        self.actionAssign_a_new_task.triggered.connect(self.assignNewTask)
        if self.isAdmin:
            self.actionAssign_a_new_task.setEnabled(True)
        self.updateTasks()



    def updateTasks(self):
        self.taskButtons=[]
        while self.verticalLayout.count():
            self.child = self.verticalLayout.takeAt(0)
            if self.child.widget():
                self.child.widget().deleteLater()
        
        self.markAsDoneButton.setEnabled(False)

        self.taskTitle.setText("") #In case the user doesn't have any tasks.
        self.taskDescription.setText("You haven't received any tasks yet. Enjoy it while it still lasts... :)")
        self.assignInfo.setText("")

        for task in taskforce_service.get_tasks(self.isAdmin):
            self.taskButtons.append(QPushButton())
            newButton = self.taskButtons[-1]
            newButton.setObjectName(str(task.task_id))
            newButton.setText(task.title)
            newButton.setCheckable(True)
            if task.done:
                newButton.setStyleSheet("background-color: green")
            else:
                newButton.setStyleSheet("background-color: red")
            newButton.clicked.connect(partial(self.updateTaskInfo,task.task_id, newButton))
            if self.selectedTaskButton == None or newButton.objectName()==self.selectedTaskButton.objectName():
                self.selectedTaskButton = newButton
                self.updateTaskInfo(task.task_id, newButton)
                newButton.setChecked(True)
            self.verticalLayout.addWidget(newButton)
        

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        

    def updateTaskInfo(self, task_id, clicked_button):
        self.selectedTaskButton.setChecked(False)
        clicked_button.setChecked(True)
        self.selectedTaskButton = clicked_button

        selected_task=taskforce_service.get_task_by_id(task_id)
        self.taskTitle.setText(selected_task.title)
        self.taskDescription.setText(selected_task.desc)
        self.markAsDoneButton.disconnect()
        self.markAsDoneButton.clicked.connect(partial(self.markAsDone,task_id))

        if self.isAdmin:
            self.assignInfo.setText(f"Assigned to: {selected_task.assigned_to.name}")
        
        else:
            self.assignInfo.setText(f"Assigned by: {selected_task.assigned_by.name}")

        if not selected_task.done:
            self.markAsDoneButton.setEnabled(True)
        else:
            self.markAsDoneButton.setEnabled(False)

    
    def markAsDone(self, task_id):
        taskforce_service.mark_as_done(task_id)
        self.updateTasks()
    
    def assignNewTask(self):
        win = NewTaskForm(self)
        win.show()
    
    def signOut(self):
        from ui.login_form import loginWindow

        self.win = loginWindow()
        self.win.show()
        self.hide()


