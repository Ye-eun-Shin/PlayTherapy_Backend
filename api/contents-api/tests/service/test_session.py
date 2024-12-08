import unittest
from unittest.mock import AsyncMock, patch
from typing import List
from datetime import datetime
from functools import wraps
from sqlalchemy.orm import Session
from contents.dto.session import SessionRequest
from contents.exception import (
    CaseNotFound,
    SessionNotFound,
    InvalidRange,
)
from contents.service.session import SessionService
from core.model.domain.session import Session as SessionDomain
from core.model.domain.state_type import StateTypeEnum
from core.repository.case import CaseRepository
from core.repository.session import SessionRepository
from core.service.security import SecurityService
from core.db.connection import ConnectionManager


class TestSessionService(unittest.TestCase):
    def setUp(self):
        self.session_repository = AsyncMock(spec=SessionRepository)
        self.case_repository = AsyncMock(spec=CaseRepository)
        self.security_service = AsyncMock(spec=SecurityService)
        self.connection_manager = AsyncMock(spec=ConnectionManager)
        self.db_session = AsyncMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.session_service = SessionService(
            session_repository=self.session_repository,
            case_repository=self.case_repository,
            security_service=self.security_service,
            connection_manager=self.connection_manager,
        )

    async def test_add(self):
        case_id = 1
        user_id = 1
        data = SessionRequest(
            data=SessionDomain(
                id=None,
                name="test",
                session_state_id=None,
                case_id=None,
                source_video_url=None,
                source_script_url=None,
                script_state_id=None,
                analyze_state_id=None,
                created_date=None,
                video_length=None,
                origin_video_url=None,
                encoding_video_url=None,
            )
        )
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=StateTypeEnum.READY,
            case_id=1,
            source_video_url=None,
            source_script_url=None,
            script_state_id=StateTypeEnum.NONE,
            analyze_state_id=StateTypeEnum.NONE,
            encoding_state_id=StateTypeEnum.NONE,
            created_date=self.session_service.get_current_date(),
            video_length=None,
            origin_video_url=None,
            encoding_video_url=None,
        )
        self.session_repository.add.return_value = session
        result = await self.session_service.add(
            case_id=case_id, user_id=user_id, data=data
        )
        self.assertEqual(result, session)
        self.db_session.commit.assert_called_once()
        self.db_session.rollback.assert_not_called()
        self.db_session.close.assert_called_once()

    async def test_get_session_found(self):
        case_id = 1
        session_id = 1
        user_id = 1
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=StateTypeEnum.READY,
            case_id=1,
            source_video_url="video.mp4",
            source_script_url="1/1/script_v1.json",
            script_state_id=StateTypeEnum.DONE,
            analyze_state_id=StateTypeEnum.NONE,
            encoding_state_id=StateTypeEnum.DONE,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="1/1/video.mp4",
            encoding_video_url="1/1/encoded_video.mp4",
        )
        self.session_repository.get.return_value = session
        result = await self.session_service.get(
            case_id=case_id, session_id=session_id, user_id=user_id
        )
        self.assertEqual(result, session)

    async def test_get_session_not_found(self):
        case_id = 1
        session_id = 1
        user_id = 1
        self.session_repository.get.return_value = None
        with self.assertRaises(SessionNotFound):
            await self.session_service.get(
                case_id=case_id, session_id=session_id, user_id=user_id
            )

    async def test_get_page_num(self):
        case_id = 1
        user_id = 1
        self.case_repository.total_count.return_value = 10
        result = self.session_service.get_page_num(case_id=case_id, user_id=user_id)
        self.assertEqual(result, 1)

    async def test_range_check_ok(self):
        skip = 0
        limit = 10
        case_id = 1
        self.session_repository.total_count.return_value = 10
        result = await self.session_service.range_check(skip, limit, case_id)
        self.assertTrue(result)

    async def test_range_check_not_ok(self):
        skip = 0
        limit = 10
        case_id = 1
        self.session_repository.total_count.return_value = 5
        result = await self.session_service.range_check(skip, limit, case_id)
        self.assertFalse(result)

    async def test_get_session_list_success(self):
        case_id = 1
        skip = 0
        limit = 10
        user_id = 1
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=StateTypeEnum.READY,
            case_id=1,
            source_video_url="video.mp4",
            source_script_url="1/1/script_v1.json",
            script_state_id=StateTypeEnum.DONE,
            analyze_state_id=StateTypeEnum.NONE,
            encoding_state_id=StateTypeEnum.DONE,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="1/1/video.mp4",
            encoding_video_url="1/1/encoded_video.mp4",
        )
        self.session_repository.total_count.return_value = 100
        self.session_repository.get_list.return_value = [session] * limit
        result = await self.session_service.get_session_list(
            case_id=case_id, skip=skip, limit=limit, user_id=user_id
        )
        self.assertEqual(result, [session] * limit)

    async def test_get_session_list_invalid_range(self):
        case_id = 1
        skip = 0
        limit = 11
        user_id = 1
        self.session_repository.total_count.return_value = 10
        with self.assertRaises(InvalidRange):
            await self.session_service.get_session_list(
                case_id=case_id, skip=skip, limit=limit, user_id=user_id
            )

    async def test_update_success(self):
        case_id = 1
        session_id = 1
        user_id = 1
        data = SessionRequest(
            data=SessionDomain(
                id=1,
                name="test",
                session_state_id=StateTypeEnum.READY,
                case_id=1,
                source_video_url="video.mp4",
                source_script_url="1/1/script_v1.json",
                script_state_id=StateTypeEnum.DONE,
                analyze_state_id=StateTypeEnum.NONE,
                encoding_state_id=StateTypeEnum.DONE,
                created_date="2024-01-01",
                video_length="00:30:00",
                origin_video_url="1/1/video.mp4",
                encoding_video_url="1/1/encoded_video.mp4",
            )
        )
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=StateTypeEnum.READY,
            case_id=1,
            source_video_url="video.mp4",
            source_script_url="1/1/script_v1.json",
            script_state_id=StateTypeEnum.DONE,
            analyze_state_id=StateTypeEnum.NONE,
            encoding_state_id=StateTypeEnum.DONE,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="1/1/video.mp4",
            encoding_video_url="1/1/encoded_video.mp4",
        )
        self.session_repository.update.return_value = True
        result = await self.session_service.update(
            case_id=case_id, session_id=session_id, user_id=user_id, data=data
        )
        self.assertEqual(result, session)
        self.db_session.commit.assert_called_once()
        self.db_session.rollback.assert_not_called()
        self.db_session.close.assert_called_once()

    async def test_update_not_found(self):
        case_id = 1
        session_id = 1
        user_id = 1
        data = SessionRequest(
            data=SessionDomain(
                id=1,
                name="test",
                session_state_id=StateTypeEnum.READY,
                case_id=1,
                source_video_url="video.mp4",
                source_script_url="1/1/script_v1.json",
                script_state_id=StateTypeEnum.DONE,
                analyze_state_id=StateTypeEnum.NONE,
                encoding_state_id=StateTypeEnum.DONE,
                created_date="2024-01-01",
                video_length="00:30:00",
                origin_video_url="1/1/video.mp4",
                encoding_video_url="1/1/encoded_video.mp4",
            )
        )
        self.session_repository.update.return_value = False
        with self.assertRaises(SessionNotFound) as e:
            await self.session_service.update(
                case_id=case_id, session_id=session_id, user_id=user_id, data=data
            )
            self.db_session.commit.assert_not_called()
            self.db_session.rollback.assert_called_once()
            self.db_session.close.assert_called_once()
        self.assertEqual(e.exception.session_id, session_id)

    async def test_delete_success(self):
        case_id = 1
        session_id = 1
        user_id = 1
        self.session_repository.delete.return_value = True
        result = await self.session_service.delete(
            case_id=case_id, session_id=session_id, user_id=user_id
        )
        self.assertTrue(result)
        self.db_session.commit.assert_called_once()
        self.db_session.rollback.assert_not_called()
        self.db_session.close.assert_called_once()

    async def test_delete_not_found(self):
        case_id = 1
        session_id = 1
        user_id = 1
        self.session_repository.delete.return_value = False
        with self.assertRaises(SessionNotFound) as e:
            await self.session_service.delete(
                case_id=case_id, session_id=session_id, user_id=user_id
            )
            self.db_session.commit.assert_not_called()
            self.db_session.rollback.assert_called_once()
            self.db_session.close.assert_called_once()
        self.assertEqual(e.exception.session_id, session_id)
