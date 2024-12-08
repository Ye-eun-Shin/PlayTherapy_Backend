import unittest
from unittest.mock import MagicMock, patch
from typing import Optional, List
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from core.model.domain.case import Case
from core.model.entity.case import CaseEntity
from core.db.connection import ConnectionManager
from core.repository.case import CaseRepository


class TestCaseRepository(unittest.TestCase):
    def setUp(self):
        self.connection_manager = MagicMock(spec=ConnectionManager)
        self.db_session = MagicMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.case_repo = CaseRepository(self.connection_manager)

    def test_add(self):
        case = Case(
            id=None,
            user_id=1,
            name="name",
            description='{"age": 6, "gender": "M"}',
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=1,
        )
        added_case = Case(
            id=None,
            user_id=1,
            name="name",
            description='{"age": 6, "gender": "M"}',
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=1,
        )
        res = self.case_repo.add(case)
        self.assertEqual(res, added_case)
        self.db_session.add.assert_called_once()
        self.db_session.commit.assert_called_once()
        self.db_session.close.assert_called_once()

    def test_get_case_found(self):
        case_id = 1
        user_id = 1
        case_entity = CaseEntity(
            id=1,
            user_id=1,
            name="name",
            description='{"age": 6, "gender": "M"}',
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=1,
        )
        self.db_session.query.return_value.join.return_value.filter.return_value.group_by.return_value.filter.return_value.first.return_value = (
            case_entity,
            1,
        )
        result = self.case_repo.get(case_id, user_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, case_id)
        self.assertEqual(result.user_id, user_id)
        self.db_session.close.assert_called_once()

    def test_get_case_not_found(self):
        case_id = 1
        user_id = 1
        self.db_session.query.return_value.join.return_value.filter.return_value.group_by.return_value.filter.return_value.first.return_value = (
            None
        )
        result = self.case_repo.get(case_id, user_id)
        self.assertIsNone(result)
        self.db_session.close.assert_called_once()

    def test_total_count_with_keyword(self):
        user_id = 1
        keyword = "keyword"
        self.db_session.query.return_value.filter.return_value.filter.return_value.count.return_value = (
            1
        )
        result = self.case_repo.total_count(user_id, keyword)
        self.assertEqual(result, 1)
        self.db_session.close.assert_called_once()

    def test_total_count_without_keyword(self):
        user_id = 1
        self.db_session.query.return_value.filter.return_value.count.return_value = 1
        result = self.case_repo.total_count(user_id)
        self.assertEqual(result, 1)
        self.db_session.close.assert_called_once()

    def test_get_list_with_keyword(self):
        user_id = 1
        skip = 0
        limit = 10
        keyword = "keyword"
        case_entity = CaseEntity(
            id=1,
            user_id=1,
            name="name",
            description='{"age": 6, "gender": "M"}',
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=1,
        )
        case_entities = [(case_entity, 1)] * 10
        self.db_session.query.return_value.join.return_value.group_by.return_value.filter.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = (
            case_entities
        )
        result = self.case_repo.get_list(user_id, skip, limit, keyword)
        self.assertEqual(len(result), 10)
        self.db_session.close.assert_called_once()

    def test_get_list_without_keyword(self):
        user_id = 1
        skip = 0
        limit = 10
        case_entity = CaseEntity(
            id=1,
            user_id=1,
            name="name",
            description='{"age": 6, "gender": "M"}',
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=1,
        )
        case_entities = [(case_entity, 1)] * 10
        self.db_session.query.return_value.join.return_value.group_by.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = (
            case_entities
        )
        result = self.case_repo.get_list(user_id, skip, limit)
        self.assertEqual(len(result), 10)
        self.db_session.close.assert_called_once()

    def test_update_success(self):
        case_id = 1
        user_id = 1
        case = Case(
            id=1,
            user_id=1,
            name="new_name",
            description='{"age": 6, "gender": "M", "new_field": "new_value"}',
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=3,
        )
        self.db_session.query.return_value.filter.return_value.update.return_value = 1
        result = self.case_repo.update(case_id, user_id, case)
        self.assertTrue(result)
        self.db_session.commit.assert_called_once()
        self.db_session.close.assert_called_once()

    def test_update_case_not_found(self):
        case_id = 1
        user_id = 1
        case = Case(
            id=1,
            user_id=1,
            name="new_name",
            description='{"age": 6, "gender": "M", "new_field": "new_value"}',
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=3,
        )
        self.db_session.query.return_value.filter.return_value.update.return_value = 0
        result = self.case_repo.update(case_id, user_id, case)
        self.assertFalse(result)
        self.db_session.commit.assert_not_called()
        self.db_session.close.assert_called_once()

    def test_delete_success(self):
        case_id = 1
        user_id = 1
        self.db_session.query.return_value.filter.return_value.delete.return_value = 1
        self.case_repo.delete(case_id, user_id)
        self.db_session.commit.assert_called_once()
        self.db_session.close.assert_called_once()

    def test_delete_not_found(self):
        case_id = 1
        user_id = 1
        self.db_session.query.return_value.filter.return_value.delete.return_value = 0
        self.case_repo.delete(case_id, user_id)
        self.db_session.commit.assert_not_called()
        self.db_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
