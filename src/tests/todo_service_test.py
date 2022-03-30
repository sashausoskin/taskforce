import unittest
import random
import string
from repositories.user_repository import User
from taskforce_service import taskforce_service, UsernameExists, WrongCredentials


class TestTaskforce(unittest.TestCase):
    def setUp(self):
        letters = string.ascii_letters

        self.name = ''.join(random.choice(letters) for i in range(10))
        self.username = ''.join(random.choice(letters) for i in range(10))
        self.password = ''.join(random.choice(letters) for i in range(10))

    def test_signup(self):
        self.assertEqual(str(taskforce_service.signup(self.name, self.username, self.password)), str(
            User(self.name, self.username, self.password)))
        taskforce_service.delete_user(self.username)

    def test_login(self):
        taskforce_service.signup(self.name, self.username, self.password)
        self.assertEqual(str(taskforce_service.login(self.username, self.password)), str(
            User(self.name, self.username, self.password)))
        taskforce_service.delete_user(self.username)

    def test_two_similiar_usernames(self):
        taskforce_service.signup(self.name, self.username, self.password)
        self.assertRaises(UsernameExists, taskforce_service.signup,
                          self.name, self.username, self.password)
        taskforce_service.delete_user(self.username)

    def test_wrong_credentials(self):
        taskforce_service.signup(self.name, self.username, self.password)
        self.assertRaises(WrongCredentials,
                          taskforce_service.login, "1", self.password)
        self.assertRaises(WrongCredentials,
                          taskforce_service.login, self.username, "1")
        taskforce_service.delete_user(self.username)

    def test_get_username(self):
        taskforce_service.signup(self.name, self.username, self.password)
        self.assertEqual(taskforce_service.get_username(), self.username)
        taskforce_service.delete_user(self.username)
