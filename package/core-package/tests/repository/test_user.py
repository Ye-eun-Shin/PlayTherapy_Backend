import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime

from core.model.entity.user import UserEntity, UserTypeEntity
from core.repository.user import UserRepository, UserTypeRepository
from core.model.domain.user import User, UserType
from core.db.connection import ConnectionManager


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.connection_manager = MagicMock(spec=ConnectionManager)
        self.db_session = MagicMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.user_repo = UserRepository(self.connection_manager)

    def test_add_user(self):
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
        self.user_repo.add(user)
        self.db_session.add.assert_called_once()
        self.db_session.commit.assert_called_once()
        self.db_session.close.assert_called_once()

    def test_get_by_id_user_found(self):
        test_id = 1
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
        self.db_session.query.return_value.filter.return_value.first.return_value = (
            user_entity
        )

        result = self.user_repo.get_by_id(test_id)
        self.assertIsNotNone(result)
        self.db_session.close.assert_called_once()

    def test_get_by_id_user_not_found(self):
        test_id = 1
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        result = self.user_repo.get_by_id(test_id)
        self.assertIsNone(result)
        self.db_session.close.assert_called_once()

    def test_get_by_email_user_found(self):
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
        self.db_session.query.return_value.filter.return_value.first.return_value = (
            user_entity
        )

        result = self.user_repo.get_by_email(test_email)
        self.assertIsNotNone(result)
        self.db_session.close.assert_called_once()

    def test_get_by_email_user_not_found(self):
        test_email = "test@example.com"
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        result = self.user_repo.get_by_email(test_email)
        self.assertIsNone(result)
        self.db_session.close.assert_called_once()

    def test_get_by_email_and_password_user_found(self):
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
        self.db_session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            user_entity
        )
        with patch(
            "core.model.domain.user.User.model_validate",
            return_value=User(
                id=1,
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
            ),
        ) as mock_model_validate:
            result = self.user_repo.get_by_email_and_password(test_email, test_password)
            mock_model_validate.assert_called_once_with(user_entity)
            self.assertIsNotNone(result)
            self.db_session.close.assert_called_once()

    def test_get_by_email_and_password_user_not_found(self):
        test_email = "test@example.com"
        test_password = "hashed_password"
        self.db_session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            None
        )
        result = self.user_repo.get_by_email_and_password(test_email, test_password)
        self.assertIsNone(result)
        self.db_session.close.assert_called_once()


class TestUserTypeRepository(unittest.TestCase):

    def setUp(self):
        self.connection_manager = MagicMock(spec=ConnectionManager)
        self.db_session = MagicMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.user_type_repo = UserTypeRepository(self.connection_manager)

    def test_list_user_types_non_empty(self):
        user_type_entity = UserTypeEntity(
            id=1,
            name="test",
        )
        user_type_entities = [user_type_entity, user_type_entity]
        self.db_session.query.return_value.all.return_value = user_type_entities
        with patch(
            "core.model.domain.user.UserType.model_validate",
            return_value=UserType(id=1, name="test_user_type"),
        ) as mock_model_validate:
            result = self.user_type_repo.list()
            self.assertEqual(mock_model_validate.call_count, len(user_type_entities))
            self.assertEqual(len(result), len(user_type_entities))
            self.db_session.close.assert_called_once()

    def test_list_user_types_empty(self):
        self.db_session.query.return_value.all.return_value = []
        result = self.user_type_repo.list()
        self.assertEqual(result, [])
        self.db_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
