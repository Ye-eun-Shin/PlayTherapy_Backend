import unittest
from unittest.mock import MagicMock, ANY
from sqlalchemy.orm import Session
from datetime import datetime

from auth.exception import UserAlreadyExist, InvalidUserEmail
from core.model.domain.user import User
from core.model.entity.user import UserEntity
from core.model.entity.org import OrgEntity
from core.model.entity.whitelist import WhiteListEntity
from core.repository.org import OrgRepository
from core.repository.user import UserRepository
from core.repository.whitelist import WhitelistRepository
from auth.service.user import UserService
from core.service.security import SecurityService
from core.db.connection import ConnectionManager


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_repository = MagicMock(spec=UserRepository)
        self.whitelist_repository = MagicMock(spec=WhitelistRepository)
        self.org_repository = MagicMock(spec=OrgRepository)
        self.security_service = MagicMock(spec=SecurityService)
        self.connection_manager = MagicMock(spec=ConnectionManager)
        self.session = MagicMock(spec=Session)
        self.connection_manager.make_session.return_value = self.session
        self.user_service = UserService(
            user_repository=self.user_repository,
            whitelist_repository=self.whitelist_repository,
            org_repository=self.org_repository,
            security_service=self.security_service,
            connection_manager=self.connection_manager,
        )

    def test_add_user_success(self):
        user = User(
            id=None,
            email="test@example.com",
            name="test",
            hashed_password="test_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        whitelist_entity = WhiteListEntity(id=1, email="test@example.com")
        self.user_service.whitelist_repository.get.return_value = whitelist_entity
        self.user_repository.get_by_email.return_value = None
        self.user_repository.add.return_value = user
        added_user = self.user_service.add(user)

        self.security_service.get_password_hash.assert_called_once()
        self.user_repository.add.assert_called_once_with(
            user=user, db_session=self.session
        )
        self.assertIsNotNone(added_user.org_id)
        self.session.commit.assert_called_once()
        self.session.rollback.assert_not_called()
        self.session.close.assert_called_once()

    def test_add_user_invalid_email(self):
        user = User(
            id=None,
            email="test@example.com",
            name="test",
            hashed_password="test_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        self.whitelist_repository.get.return_value = None
        with self.assertRaises(InvalidUserEmail):
            self.user_service.add(user)
            self.session.commit.assert_not_called()
            self.session.rollback.assert_called_once()
            self.session.close.assert_called_once()

    def test_add_user_already_exist(self):
        user = User(
            id=None,
            email="test@example.com",
            name="test",
            hashed_password="test_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        whitelist_entity = WhiteListEntity(id=1, email="test@example.com")
        user_entity = UserEntity(
            email="test@example.com",
            name="test",
            hashed_password="test_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        self.user_service.whitelist_repository.get.return_value = whitelist_entity
        self.user_repository.get_by_email.return_value = user_entity
        with self.assertRaises(UserAlreadyExist):
            self.user_service.add(user)
            self.session.commit.assert_not_called()
            self.session.rollback.assert_called_once()
            self.session.close.assert_called_once()

    def test_get_by_email_found(self):
        test_email = "test@example.com"
        user_entity = UserEntity(
            email="test@example.com",
            name="test",
            hashed_password="test_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        self.user_repository.get_by_email.return_value = user_entity
        result = self.user_service.get_by_email(test_email)
        self.assertEqual(result, user_entity)

    def test_get_by_email_not_found(self):
        test_email = "test@example.com"
        self.user_repository.get_by_email.return_value = None
        result = self.user_service.get_by_email(test_email)
        self.assertIsNone(result)

    def test_get_by_email_and_password_found(self):
        test_email = "test@example.com"
        test_password = "test_password"
        user_entity = UserEntity(
            email="test@example.com",
            name="test",
            hashed_password="hashed_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        self.user_repository.get_by_email.return_value = user_entity
        self.security_service.verify_password.return_value = True
        result = self.user_service.get_by_email_and_password(test_email, test_password)
        self.assertEqual(result, user_entity)

    def test_get_by_email_and_password_email_not_found(self):
        test_email = "test@example.com"
        test_password = "test_password"
        self.user_repository.get_by_email.return_value = None
        result = self.user_service.get_by_email_and_password(test_email, test_password)
        self.assertIsNone(result)

    def test_get_by_email_and_password_password_not_match(self):
        test_email = "test@example.com"
        test_password = "test_password"
        user_entity = UserEntity(
            email="test@example.com",
            name="test",
            hashed_password="hashed_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        self.user_repository.get_by_email.return_value = user_entity
        self.security_service.verify_password.return_value = False
        result = self.user_service.get_by_email_and_password(test_email, test_password)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
