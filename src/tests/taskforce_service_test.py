from curses.ascii import US
from datetime import datetime
import unittest
import random
import string
from entities.notification import Notification
from entities.task import Task
from entities.comment import Comment
from repositories.user_repository import User
from services.user_service import user_service, UsernameExists, WrongCredentials
from services.org_service import org_service, InvalidCode, OrgExists
from services.task_service import task_service


class TestTaskforce(unittest.TestCase):
    def setUp(self):
        self.letters = string.ascii_letters

        self.admin_name = ''.join(random.choice(self.letters)
                                  for i in range(10))
        self.admin_username = ''.join(
            random.choice(self.letters) for i in range(10))
        self.admin_password = ''.join(
            random.choice(self.letters) for i in range(10))

        self.name = ''.join(random.choice(self.letters) for i in range(10))
        self.username = ''.join(random.choice(self.letters) for i in range(10))
        self.password = ''.join(random.choice(self.letters) for i in range(10))

        self.org_name = ''.join(random.choice(self.letters) for i in range(10))
        self.org_code = ''.join(random.choice(self.letters) for i in range(10))

        self.user = user_service.signup(
            self.name, self.username, self.password)

        self.admin = user_service.signup(
            self.admin_name, self.admin_username, self.admin_password)

        self.org = org_service.create_org(self.org_name, self.org_code)

    def tearDown(self) -> None:
        # Make sure that there are no remaining notifications
        user_service.login(self.admin_username, self.admin_password)
        task_service.check_notifications()
        user_service.login(self.username, self.password)
        task_service.check_notifications()

        task_service.delete_users_comments(self.user)
        task_service.delete_users_comments(self.admin)
        task_service.delete_tasks()
        org_service.delete_org(self.org.id)
        user_service.delete_user(self.username)
        user_service.delete_user(self.admin_username)
        user_service.signout()
        task_service.signout()
        org_service.signout()

    def test_signup(self):
        self.assertEqual(str(self.user), str(
            User(self.name, self.username, self.password)))

    def test_login(self):
        self.assertEqual(str(user_service.login(self.username, self.password)), str(
            User(self.name, self.username, self.password)))

    def test_two_similiar_usernames(self):
        self.assertRaises(UsernameExists, user_service.signup,
                          self.name, self.username, self.password)

    def test_wrong_credentials(self):
        self.assertRaises(WrongCredentials,
                          user_service.login, "1", self.password)
        self.assertRaises(WrongCredentials,
                          user_service.login, self.username, "1")

    def test_create_org(self):
        self.assertEqual(str(self.org), str(
            f"Name: {self.org_name}, Code: {self.org_code}"))

    def test_org_exists_error(self):
        self.assertRaises(OrgExists, org_service.create_org,
                          self.org_name, self.org_code)

    def test_join_org(self):
        org_service.join_org(self.org_code)
        self.assertEqual(org_service.get_orgs()[0], self.org)

    def test_invalid_code(self):
        temp_code = ''.join(random.choice(string.ascii_letters)
                            for i in range(10))
        self.assertRaises(InvalidCode, org_service.join_org, temp_code)

    def test_is_admin(self):
        self.assertEqual(org_service.is_admin(), True)
        user_service.login(self.username, self.password)
        org_service.join_org(self.org.code)
        self.assertEqual(org_service.is_admin(), False)

    def test_get_members(self):
        user_service.login(self.username, self.password)
        org_service.join_org(self.org.code)
        self.assertEqual(str(org_service.get_all_members_in_current_org()[0]), str(
            User(self.user.name, self.user.username, "")))
        self.assertEqual(len(org_service.get_all_members_in_current_org()), 1)

    def test_assign_task(self):
        user_service.login(self.username, self.password)
        org_service.join_org(self.org.code)
        user_service.login(self.admin_username, self.admin_password)
        task_service.assign_task(self.user, "TEST", "TEST")
        self.assertEqual(str(task_service.get_tasks()[0]), str(Task("TEST", "TEST", User(
            self.admin.name, self.admin.username, ""), User(self.name, self.username, ""), datetime.now())))
        user_service.login(self.username, self.password)
        self.assertEqual(str(task_service.get_tasks()[0]), str(Task("TEST", "TEST", User(
            self.admin.name, self.admin_username, ""), User(self.name, self.username, ""), datetime.now())))

    def test_mark_as_done(self):
        user_service.login(self.username, self.password)
        org_service.join_org(self.org.code)
        user_service.login(self.admin_username, self.admin_password)
        task_service.assign_task(self.user, "TEST_DONE", "TEST_DONE")
        user_service.login(self.username, self.password)
        task = task_service.get_tasks()[0]
        self.assertEqual(task.done_on, None)
        task_service.mark_as_done(task)
        user_service.login(self.admin_username, self.admin_password)
        task = task_service.get_tasks()[0]
        self.assertNotEqual(task.done_on, None)

    def test_notifications(self):
        task_service.send_notification(
            self.user, "TEST_NOTIFICATION", "test")
        user_service.login(self.username, self.password)
        self.assertEqual(str(task_service.check_notifications()[0]), str(
            Notification("TEST_NOTIFICATION", "test")))
        self.assertEqual(task_service.check_notifications(), [])

    def test_add_as_admin(self):
        user_service.login(self.username, self.password)
        org_service.join_org(self.org_code)
        self.assertEqual(org_service.is_admin(), False)
        user_service.login(self.admin_username, self.admin_password)
        org_service.make_admin_in_current_org(self.user)
        user_service.login(self.username, self.password)
        self.assertEqual(org_service.is_admin(), True)

    def test_change_org(self):
        self.assertEqual(org_service.get_current_org(), self.org)

        new_org_name = ''.join(random.choice(self.letters) for i in range(10))
        new_org_code = ''.join(random.choice(self.letters) for i in range(10))

        new_org = org_service.create_org(new_org_name, new_org_code)

        self.assertEqual(org_service.get_current_org(), new_org)

        org_service.set_current_org(self.org)

        self.assertEqual(org_service.get_current_org(), self.org)

        org_service.delete_org(new_org.id)

    def test_get_orgs(self):
        user_service.login(self.username, self.password)
        org_service.join_org(self.org_code)
        self.assertEqual(str(org_service.get_orgs()[0]), str(self.org))

    def test_filters(self):
        user_service.login(self.username, self.password)
        org_service.join_org(self.org_code)
        user_service.login(self.admin_username, self.admin_password)
        task_service.assign_task(self.user, "TEST_FILTER", "TEST_FILTER")
        task = task_service.get_tasks()[0]
        task_service.mark_as_done(task)
        self.assertEqual(str(task_service.get_tasks()[0].title), task.title)
        self.assertEqual(task_service.get_tasks(["undone"]), [])
        self.assertEqual(task_service.get_tasks(
            ["user_assigned"])[0].title, task.title)

    def test_comments(self):
        user_service.login(self.username, self.password)
        org_service.join_org(self.org_code)

        user_service.login(self.admin_username, self.admin_password)
        task_service.assign_task(
            self.user, "TEST_COMMENT_TASK", "TEST_COMMENT_TASK")
        task = task_service.get_tasks()[0]
        task_service.post_comment(task, "TEST_COMMENT_MESSAGE")
        task_service.update_comments_in_memory()
        self.assertEqual(str(task_service.get_comments_from_memory()[task.id][0]), str(
            Comment(task.id, "TEST_COMMENT_MESSAGE", None, self.admin)))
