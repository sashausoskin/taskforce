from datetime import datetime
from functools import partial
from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon
from taskforce_service import taskforce_service
from ui.messages import notify, success

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

        self.actionSign_out.triggered.connect(self.signOut)
        self.actionAssign_a_new_task.triggered.connect(self.assignNewTask)

        self.updateOrgInformation()

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
        self.assignedDate.setText("")
        self.doneDate.setText("")

        for task in taskforce_service.get_tasks():
            self.taskButtons.append(QPushButton())
            self.newButton = self.taskButtons[-1]
            self.newButton.setObjectName(str(task.task_id))
            self.newButton.setText(task.title)
            self.newButton.setCheckable(True)
            if task.done_on:
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

        if not selected_task.done_on and self.isAdmin == False:
            self.markAsDoneButton.setEnabled(True)
        else:
            self.markAsDoneButton.setEnabled(False)
        
        task_age = datetime.now()-selected_task.assigned_on
        
        self.assignedDate.setText(f"Assigned on: {selected_task.assigned_on.strftime('%d.%m.%Y %H:%M')} ({self.calculateAgeText(task_age)})")


        if selected_task.done_on:
            done_age = datetime.now()-selected_task.done_on
            self.doneDate.setText(f"Done on: {selected_task.done_on.strftime('%d.%m.%Y %H:%M')} ({self.calculateAgeText(done_age)})")
        else:
            self.doneDate.setText("")
    
    def calculateAgeText(self, time):
        task_age = time
        if task_age.total_seconds()<60:
            if task_age.seconds == 1:
                return "1 second ago"
            return f"{task_age.seconds} seconds ago"
        if task_age.total_seconds()/60<60:
            if task_age.total_seconds()//60 == 1:
                return "1 minute ago"
            return f"{task_age.seconds//60} minutes ago"
        if task_age.total_seconds()/60/60<24:
            if task_age.seconds/60//60== 1:
                return "1 hour ago"
            return f"{task_age.seconds//60//60} hours ago"
        if task_age.total_days()<7:
            if task_age.days == 1:
                return "1 day ago"
            return f"{task_age.days} days ago"
        if task_age.total_months()<12:
            if task_age.months == 1:
                return "1 month ago"
            return f"{task_age.months} months ago"
        else:
            if task_age.years == 1:
                return "1 year ago"
            return f"{task_age.years} years ago"


    def markAsDone(self, task, assigned_to):
        self.statusbar.showMessage("Marking task as done...")
        taskforce_service.mark_as_done(task)
        taskforce_service.send_notification(
            assigned_to, f"User {taskforce_service.get_name()} has finished a task: {task.title}", "A task has been finished")
        self.updateTasks()

    def assignNewTask(self):
        win = NewTaskForm(self)
        win.show()

    def openJoinOrgForm(self):
        from ui.org_join import OrgJoinWindow

        win = OrgJoinWindow()
        
        win.WindowTitle.setText(
            "Join an organization by entering a code below or create a new organization")
        win.org_create_form.buttonBox.accepted.connect(
            self.updateOrgInformation)
        win.org_create_form.buttonBox.accepted.connect(win.close)
        win.org_create_form.buttonBox.accepted.connect(
            win.org_create_form.close)
        win.show()

    def updateOrgInformation(self):
        # Clear the current member and organization selection
        self.menuAssign_a_member_as_admin.clear()
        self.menuChange_current_organization.clear()


        self.current_org = taskforce_service.get_current_org()
        self.isAdmin = taskforce_service.is_admin()

        self.setWindowTitle(f"TaskForce - {self.current_org.name}")
        self.nameLabel.setText(f"{taskforce_service.get_name()}")
        if self.isAdmin:
            self.orgLabel.setText(
                f"{self.current_org.name} (Admin)")
        else:
            self.orgLabel.setText(
                f"{self.current_org.name} (Member)")
        self.selectedTaskButton = None

        if self.isAdmin:
            self.actionAssign_a_new_task.setEnabled(True)
            self.menuAssign_a_member_as_admin.setEnabled(True)
        
        else:
            self.actionAssign_a_new_task.setEnabled(False)
            self.menuAssign_a_member_as_admin.setEnabled(False)

        self.actionJoin_organization_or_create_a_new_one.triggered.connect(
            self.openJoinOrgForm)

        for org in taskforce_service.get_orgs():
            changeOrgTo = QtWidgets.QAction(self)
            changeOrgTo.setObjectName(f"org_{org.id}")
            changeOrgTo.triggered.connect(partial(self.setCurrentOrg, org))
            self.menuChange_current_organization.addAction(changeOrgTo)
            changeOrgTo.setText(org.name)

        members = taskforce_service.get_all_members_in_org()
        for member in members:
            addAdminButton = QtWidgets.QAction(self)
            addAdminButton.setObjectName(f"member_{member.id}")
            self.menuAssign_a_member_as_admin.addAction(addAdminButton)
            addAdminButton.setText(member.name)
            addAdminButton.triggered.connect(partial(self.addAsAdmin, member))
        
        self.updateTasks()

    def signOut(self):
        from ui.login_form import loginWindow

        self.notificationChecker.stopNotificationCheck = True

        self.win = loginWindow()
        self.win.show()
        self.hide()

    def addAsAdmin(self, member):
        taskforce_service.make_admin_in_current_org(member.id)
        taskforce_service.send_notification(
            member, f"You have been promototed to an admin status over at {self.current_org.name}",
            "You have been promoted")
        success("Succesfully added admin",
                f"{member.name} is now an admin in your organization! ")
        self.updateOrgInformation()
    
    def setCurrentOrg(self, org):
        taskforce_service.set_current_org(org)
        self.updateOrgInformation()

