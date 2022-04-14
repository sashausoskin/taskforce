from curses.ascii import US
from datetime import datetime
import unittest
import random
import string
from entities.notification import Notification
from entities.task import Task
from repositories.user_repository import User
from taskforce_service import InvalidCode, taskforce_service, UsernameExists, WrongCredentials, OrgExists


class TestTaskforce(unittest.TestCase):
    def setUp(self):
        letters = string.ascii_letters

        self.admin_name = ''.join(random.choice(letters) for i in range(10))
        self.admin_username = ''.join(
            random.choice(letters) for i in range(10))
        self.admin_password = ''.join(
            random.choice(letters) for i in range(10))

        self.name = ''.join(random.choice(letters) for i in range(10))
        self.username = ''.join(random.choice(letters) for i in range(10))
        self.password = ''.join(random.choice(letters) for i in range(10))

        self.org_name = ''.join(random.choice(letters) for i in range(10))
        self.org_code = ''.join(random.choice(letters) for i in range(10))

        self.user = taskforce_service.signup(
            self.name, self.username, self.password)

        self.admin = taskforce_service.signup(
            self.admin_name, self.admin_username, self.admin_password)

        self.org = taskforce_service.create_org(self.org_name, self.org_code)

    def tearDown(self) -> None:
        # Make sure that there are no remaining notifications
        taskforce_service.login(self.admin.username, self.admin.password)
        taskforce_service.check_notifications()
        taskforce_service.login(self.user.username, self.user.password)
        taskforce_service.check_notifications()

        taskforce_service.delete_tasks()
        taskforce_service.delete_org(self.org.id)
        taskforce_service.delete_user(self.username)
        taskforce_service.signout()

    def test_signup(self):
        self.assertEqual(str(self.user), str(
            User(self.name, self.username, self.password)))

    def test_login(self):
        self.assertEqual(str(taskforce_service.login(self.username, self.password)), str(
            User(self.name, self.username, self.password)))

    def test_two_similiar_usernames(self):
        self.assertRaises(UsernameExists, taskforce_service.signup,
                          self.name, self.username, self.password)

    def test_wrong_credentials(self):
        self.assertRaises(WrongCredentials,
                          taskforce_service.login, "1", self.password)
        self.assertRaises(WrongCredentials,
                          taskforce_service.login, self.username, "1")

    def test_get_username(self):
        self.assertEqual(taskforce_service.get_username(), self.admin.username)

    def test_get_name(self):
        self.assertEqual(taskforce_service.get_name(), self.admin.name)

    def test_create_org(self):
        self.assertEqual(str(self.org), str(
            f"Name: {self.org_name}, Code: {self.org_code}"))

    def test_org_exists_error(self):
        self.assertRaises(OrgExists, taskforce_service.create_org,
                          self.org_name, self.org_code)

    def test_join_org(self):
        taskforce_service.join_org(self.org_code)
        self.assertEqual(taskforce_service.get_orgs()[0], self.org)

    def test_invalid_code(self):
        temp_code = ''.join(random.choice(string.ascii_letters)
                            for i in range(10))
        self.assertRaises(InvalidCode, taskforce_service.join_org, temp_code)

    def test_is_admin(self):
        self.assertEqual(taskforce_service.is_admin(), True)
        taskforce_service.login(self.user.username, self.user.password)
        taskforce_service.join_org(self.org.code)
        self.assertEqual(taskforce_service.is_admin(), False)

    def test_get_members(self):
        taskforce_service.login(self.user.username, self.user.password)
        taskforce_service.join_org(self.org.code)
        self.assertEqual(str(taskforce_service.get_all_members_in_org()[0]), str(
            User(self.user.name, self.user.username, "")))
        self.assertEqual(len(taskforce_service.get_all_members_in_org()), 1)

    def test_assign_task(self):
        taskforce_service.login(self.user.username, self.user.password)
        taskforce_service.join_org(self.org.code)
        taskforce_service.login(self.admin.username, self.admin.password)
        taskforce_service.assign_task(self.user, "TEST", "TEST")
        self.assertEqual(str(taskforce_service.get_tasks()[0]), str(Task("TEST", "TEST", User(
            self.admin.name, self.admin.username, ""), User(self.name, self.username, ""), datetime.now())))
        taskforce_service.login(self.user.username, self.user.password)
        self.assertEqual(str(taskforce_service.get_tasks()[0]), str(Task("TEST", "TEST", User(
            self.admin.name, self.admin.username, ""), User(self.name, self.username, ""), datetime.now())))

    def test_get_task_by_id(self):
        taskforce_service.assign_task(self.user, "TEST_ID", "TEST_ID")
        test_task = taskforce_service.get_tasks()[0]
        self.assertEqual(
            test_task, taskforce_service.get_task_by_id(test_task.task_id))
        self.assertEqual(None, taskforce_service.get_task_by_id(0))

    def test_mark_as_done(self):
        taskforce_service.login(self.user.username, self.user.password)
        taskforce_service.join_org(self.org.code)
        taskforce_service.login(self.admin.username, self.admin.password)
        taskforce_service.assign_task(self.user, "TEST_DONE", "TEST_DONE")
        taskforce_service.login(self.user.username, self.user.password)
        task = taskforce_service.get_tasks()[0]
        self.assertEqual(task.done_on, None)
        taskforce_service.mark_as_done(task)
        taskforce_service.login(self.admin.username, self.admin.password)
        task = taskforce_service.get_tasks()[0]
        self.assertNotEqual(task.done_on, None)

    def test_notifications(self):
        taskforce_service.send_notification(
            self.user, "TEST_NOTIFICATION", "test")
        taskforce_service.login(self.user.username, self.user.password)
        self.assertEqual(str(taskforce_service.check_notifications()[0]), str(
            Notification("TEST_NOTIFICATION", "test")))
        self.assertEqual(taskforce_service.check_notifications(), [])
