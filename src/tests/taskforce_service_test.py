import unittest
import random
import string
from repositories.user_repository import User
from taskforce_service import InvalidCode, taskforce_service, UsernameExists, WrongCredentials, OrgExists


class TestTaskforce(unittest.TestCase):
    def setUp(self):
        letters = string.ascii_letters

        self.name = ''.join(random.choice(letters) for i in range(10))
        self.username = ''.join(random.choice(letters) for i in range(10))
        self.password = ''.join(random.choice(letters) for i in range(10))

        self.org_name = ''.join(random.choice(letters) for i in range(10))
        self.org_code = ''.join(random.choice(letters) for i in range(10))

        self.user = taskforce_service.signup(
            self.name, self.username, self.password)

        self.org = taskforce_service.create_org(self.org_name, self.org_code)

    def tearDown(self) -> None:
        taskforce_service.delete_org(self.org.id)
        taskforce_service.delete_user(self.username)

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
        self.assertEqual(taskforce_service.get_username(), self.username)

    def test_get_name(self):
        self.assertEqual(taskforce_service.get_name(), self.name)

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
