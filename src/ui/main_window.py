from functools import partial
from time import sleep
from typing import Any
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon
from taskforce_service import taskforce_service
from ui.messages import notify

from ui.main_window_ui import Ui_MainWindow
from ui.new_task import NewTaskForm


class NotificationChecker(QObject):

    update_signal = pyqtSignal()

    def __init__(self, parent=None) -> None:
        self.stopNotificationCheck = False
        super().__init__(parent)

    @pyqtSlot()
    def run(self):

        while not self.stopNotificationCheck:
            notifications = taskforce_service.check_notifications()

            for notification in notifications:
                notify(notification)

            if len(notifications) > 0:
                self.update_signal.emit()

            sleep(2)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle("TaskForce")
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.notificationChecker = NotificationChecker()
        self.notificationChecker.update_signal.connect(self.updateTasks)
        self.thread = QThread(self)
        self.notificationChecker.moveToThread(self.thread)
        self.thread.started.connect(self.notificationChecker.run)
        self.thread.start()

        self.isAdmin = taskforce_service.is_admin()
        self.nameLabel.setText(f"{taskforce_service.get_name()}")
        if self.isAdmin:
            self.orgLabel.setText(
                f"{taskforce_service.get_orgs()[0].name} (Admin)")
        else:
            self.orgLabel.setText(
                f"{taskforce_service.get_orgs()[0].name} (Member)")
        self.selectedTaskButton = None
        self.actionSign_out.triggered.connect(self.signOut)
        self.actionAssign_a_new_task.triggered.connect(self.assignNewTask)
        if self.isAdmin:
            self.actionAssign_a_new_task.setEnabled(True)
        self.updateTasks()

    pyqtSlot()

    def updateTasks(self):
        self.statusbar.showMessage("Fetching tasks...")
        self.taskButtons = []
        selectedButtonName = None

        if self.selectedTaskButton:
            selectedButtonName = self.selectedTaskButton.objectName()
        while self.verticalLayout.count():
            self.child = self.verticalLayout.takeAt(0)
            if self.child.widget():
                self.child.widget().deleteLater()

        self.markAsDoneButton.setEnabled(False)

        self.taskTitle.setText("")  # In case the user doesn't have any tasks.
        if self.isAdmin:
            self.taskDescription.setText(
                "You haven't given out any tasks yet. Make sure not to keep the others bored for too long... :)")
        else:
            self.taskDescription.setText(
                "You haven't received any tasks yet. Enjoy it while it still lasts... :)")
        self.assignInfo.setText("")

        for task in taskforce_service.get_tasks():
            self.taskButtons.append(QPushButton())
            self.newButton = self.taskButtons[-1]
            self.newButton.setObjectName(str(task.task_id))
            self.newButton.setText(task.title)
            self.newButton.setCheckable(True)
            if task.done:
                self.newButton.setStyleSheet("background-color: green")
            else:
                self.newButton.setStyleSheet("background-color: red")
            self.newButton.clicked.connect(
                partial(self.updateTaskInfo, task, self.newButton))
            if self.selectedTaskButton == None or self.newButton.objectName() == selectedButtonName:
                self.selectedTaskButton = self.newButton
                self.updateTaskInfo(task, self.newButton)
                self.newButton.setChecked(True)
            self.verticalLayout.addWidget(self.newButton)

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.statusbar.clearMessage()

    def updateTaskInfo(self, task, clicked_button):
        self.selectedTaskButton.setChecked(False)
        clicked_button.setChecked(True)
        self.selectedTaskButton = clicked_button

        selected_task = taskforce_service.get_task_by_id(task.task_id)
        self.taskTitle.setText(selected_task.title)
        self.taskDescription.setText(selected_task.desc)
        self.markAsDoneButton.disconnect()
        self.markAsDoneButton.clicked.connect(
            partial(self.markAsDone, task, task.assigned_by))

        if self.isAdmin:
            self.assignInfo.setText(f"Assigned to: {task.assigned_to.name}")

        else:
            self.assignInfo.setText(f"Assigned by: {task.assigned_by.name}")

        if not selected_task.done and self.isAdmin == False:
            self.markAsDoneButton.setEnabled(True)
        else:
            self.markAsDoneButton.setEnabled(False)

    def markAsDone(self, task, assigned_to):
        self.statusBar.showMessage("Marking task as done...")
        taskforce_service.mark_as_done(task)
        taskforce_service.send_notification(
            assigned_to, f"User {taskforce_service.get_name()} has finished a task: {task.title}", "done")
        self.updateTasks()

    def assignNewTask(self):
        win = NewTaskForm(self)
        win.show()

    def signOut(self):
        from ui.login_form import loginWindow

        self.notificationChecker.stopNotificationCheck = True

        self.win = loginWindow()
        self.win.show()
        self.hide()
