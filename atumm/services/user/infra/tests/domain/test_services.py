from unittest.mock import patch

from atumm.services.user.domain.services import PasswordHasher
from faker import Faker


class TestPasswordHasher:
    faker = Faker()

    def setup_method(self):
        self.password_key = self.faker.password()
        self.password_hasher = PasswordHasher(self.password_key)

    def test_generate_salt(self):
        salt = self.password_hasher.generate_salt()
        assert isinstance(salt, str)
        assert len(salt) > 26

    def test_hash_password(self):
        password = self.faker.password()
        salt = self.password_hasher.generate_salt()

        with patch(
            "atumm.services.user.domain.services.hashpw",
            return_value=b"hashed_password",
        ):
            hashed_password = self.password_hasher.hash_password(password, salt)

        assert hashed_password == b"hashed_password"

    def test_is_password_valid(self):
        password = self.faker.password()
        salt = self.password_hasher.generate_salt()
        hashed_password = self.password_hasher.hash_password(password, salt)

        self.password_hasher.password = b"hashed_password"
        is_valid = self.password_hasher.is_password_valid(
            password, hashed_password, salt
        )

        assert is_valid
