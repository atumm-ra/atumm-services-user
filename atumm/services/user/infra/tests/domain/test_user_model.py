import unittest

from faker import Faker

from atumm.services.user.domain.models import StatusEnum, UserModel


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = UserModel(
            email=self.faker.email(),
            password=self.faker.password(length=10),
            username=self.faker.user_name(),
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
        )

    def test_lock(self):
        self.user.lock()
        self.assertTrue(self.user.is_locked())

    def test_is_not_locked(self):
        self.assertFalse(self.user.is_locked())


if __name__ == "__main__":
    unittest.main()
