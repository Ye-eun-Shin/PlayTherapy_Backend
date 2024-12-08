import unittest
from unittest.mock import AsyncMock, patch
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from contents.dto.case import CaseRequest
from contents.exception import (
    CaseNotFound,
    InvalidRange,
)
from contents.service.case import CaseService
from core.model.domain.case import Case
from core.repository.case import CaseRepository
from core.service.security import SecurityService
from core.db.connection import ConnectionManager


class TestCaseService(unittest.TestCase):
    def setUp(self):
        self.case_repository = AsyncMock(spec=CaseRepository)
        self.security_service = AsyncMock(spec=SecurityService)
        self.connection_manager = AsyncMock(spec=ConnectionManager)
        self.db_session = AsyncMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.case_service = CaseService(
            case_repository=self.case_repository,
            security_service=self.security_service,
            connection_manager=self.connection_manager,
        )

    async def test_add(self):
        user_id = 1
        case_request = CaseRequest(
            id=None,
            name="name",
            description={"age": 6, "gender": "M"},
            user_id=None,
            start_date=None,
            updated_date=None,
            case_state_id=None,
        )
        case = Case(
            id=None,
            user_id=user_id,
            start_date=self.case_service.get_current_date(),
            updated_date=self.case_service.get_current_date(),
            name="name",
            description='{"age": 6, "gender": "M"}',
            session_count=0,
            case_state_id=1,
        )
        self.case_repository.add.return_value = case
        result = await self.case_service.add(user_id, case_request)
        self.assertEqual(result, case)
        self.db_session.commit.assert_called_once()
        self.db_session.rollback.assert_not_called()
        self.db_session.close.assert_called_once()

    async def test_get_case_found(self):
        case_id = 1
        user_id = 1
        case = Case(
            id=1,
            user_id=1,
            name="name",
            description='{"age": 6, "gender": "M"}',
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=2,
        )
        self.case_repository.get.return_value = case
        result = await self.case_service.get(case_id, user_id)
        self.assertEqual(result, case)

    async def test_get_case_not_found(self):
        case_id = 1
        user_id = 1
        self.case_repository.get.return_value = None
        with self.assertRaises(CaseNotFound) as e:
            await self.case_service.get(case_id, user_id)
        self.assertEqual(e.exception.case_id, case_id)

    async def test_get_page_num(self):
        user_id = 1
        keyword = "keyword"
        self.case_repository.total_count.return_value = 10
        result = await self.case_service.get_page_num(user_id, keyword)
        self.assertEqual(result, 1)

    async def test_range_check_ok(self):
        skip = 0
        limit = 10
        user_id = 1
        keyword = "keyword"
        self.case_repository.total_count.return_value = 10
        result = await self.case_service.range_check(skip, limit, user_id, keyword)
        self.assertTrue(result)

    async def test_range_check_invalid(self):
        skip = 0
        limit = 11
        user_id = 1
        keyword = "keyword"
        self.case_repository.total_count.return_value = 10
        result = await self.case_service.range_check(skip, limit, user_id, keyword)
        self.assertFalse(result)

    async def test_get_case_list(self):
        skip = 0
        limit = 10
        user_id = 1
        keyword = "keyword"
        case = Case(
            id=1,
            user_id=1,
            name="keyword_name",
            description='{"age": 6, "gender": "M"}',
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=2,
        )
        self.case_repository.range_check.return_value = True
        self.case_repository.get_list.return_value = [case] * (limit - skip)
        result = await self.case_service.get_case_list(skip, limit, user_id, keyword)
        self.assertEqual(len(result), limit - skip)

    async def test_get_case_list_invalid_range(self):
        skip = 0
        limit = 11
        user_id = 1
        keyword = "keyword"
        self.case_repository.range_check.return_value = False
        with self.assertRaises(InvalidRange) as e:
            await self.case_service.get_case_list(skip, limit, user_id, keyword)
        self.assertEqual(e.exception.skip, skip)
        self.assertEqual(e.exception.limit, limit)

    async def test_update_success(self):
        user_id = 1
        case_id = 1
        case_request = CaseRequest(
            id=1,
            user_id=1,
            name="updated_name",
            description={"age": 6, "gender": "M"},
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=3,
        )
        case = Case(
            id=1,
            user_id=1,
            name="updated_name",
            description='{"age": 6, "gender": "M"}',
            session_count=0,
            start_date="2024-01-01",
            updated_date=self.case_service.get_current_date(),
            case_state_id=3,
        )
        self.case_repository.update.return_value = case
        result = await self.case_service.update(user_id, case_id, case_request)
        self.assertTrue(result)
        self.db_session.commit.assert_called_once()
        self.db_session.rollback.assert_not_called()
        self.db_session.close.assert_called_once()

    async def test_update_case_not_found(self):
        user_id = 1
        case_id = 1
        case_request = CaseRequest(
            id=1,
            user_id=1,
            name="updated_name",
            description={"age": 6, "gender": "M"},
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=3,
        )
        self.case_repository.get.return_value = False
        with self.assertRaises(CaseNotFound) as e:
            await self.case_service.update(user_id, case_id, case_request)
            self.db_session.commit.assert_not_called()
            self.db_session.rollback.assert_called_once()
            self.db_session.close.assert_called_once()
        self.assertEqual(e.exception.case_id, case_id)

    async def test_delete_success(self):
        user_id = 1
        case_id = 1
        case = Case(
            id=1,
            user_id=1,
            name="name",
            description='{"age": 6, "gender": "M"}',
            session_count=0,
            start_date="2024-01-01",
            updated_date="2024-01-01",
            case_state_id=2,
        )
        self.case_repository.get.return_value = case
        result = await self.case_service.delete(user_id, case_id)
        self.assertTrue(result)
        self.db_session.commit.assert_called_once()
        self.db_session.rollback.assert_not_called()
        self.db_session.close.assert_called_once()

    async def test_delete_case_not_found(self):
        user_id = 1
        case_id = 1
        self.case_repository.get.return_value = None
        with self.assertRaises(CaseNotFound) as e:
            await self.case_service.delete(user_id, case_id)
            self.db_session.commit.assert_not_called()
            self.db_session.rollback.assert_called_once()
            self.db_session.close.assert_called_once()
        self.assertEqual(e.exception.case_id, case_id)
