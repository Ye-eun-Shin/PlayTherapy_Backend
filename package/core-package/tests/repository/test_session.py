import unittest
from unittest.mock import MagicMock, patch
from typing import Optional, List
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from core.model.domain.session import Session as SessionDomain
from core.model.domain.state_type import StateTypeEnum
from core.model.entity.session import SessionEntity
from core.db.connection import ConnectionManager
from core.repository.session import SessionRepository


class TestSessionRepository(unittest.TestCase):
    def setUp(self):
        self.connection_manager = MagicMock(spec=ConnectionManager)
        self.db_session = MagicMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.session_repo = SessionRepository(self.connection_manager)

    def test_add(self):
        session = SessionDomain(
            id=None,
            name="test",
            session_state_id=1,
            case_id=1,
            source_video_url=None,
            source_script_url=None,
            script_state_id=1,
            analyze_state_id=1,
            created_date="2024-01-01",
            video_length=None,
            origin_video_url=None,
            encoding_video_url=None,
        )
        result = self.session_repo.add(session)
        self.assertEqual(result, session)
        self.db_session.add.assert_called_once()
        self.db_session.commit.assert_called_once()
        self.db_session.close.assert_called_once()

    def test_get_session_found(self):
        session_id = 1
        session_entity = SessionEntity(
            id=1,
            name="test",
            session_state_id=1,
            case_id=1,
            source_video_url="/source/video.mp4",
            source_script_url="/source/script.json",
            script_state_id=1,
            analyze_state_id=1,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="/origin/video.mp4",
            encoding_video_url="/encoding/video.mp4",
        )
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=1,
            case_id=1,
            source_video_url="/source/video.mp4",
            source_script_url="/source/script.json",
            script_state_id=1,
            analyze_state_id=1,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="/origin/video.mp4",
            encoding_video_url="/encoding/video.mp4",
        )
        self.db_session.query.return_value.filter.return_value.first.return_value = (
            session_entity
        )
        result = self.session_repo.get(session_id)
        self.assertIsNotNone(result)
        self.assertEqual(result, session)
        self.db_session.close.assert_called_once()

    def test_get_session_not_found(self):
        session_id = 1
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        result = self.session_repo.get(session_id)
        self.assertIsNone(result)
        self.db_session.close.assert_called_once()

    def test_total_count_with_keyword(self):
        case_id = 1
        keyword = "keyword"
        self.db_session.query.return_value.filter.return_value.filter.return_value.count.return_value = (
            1
        )
        result = self.session_repo.total_count(case_id, keyword)
        self.assertEqual(result, 1)
        self.db_session.close.assert_called_once()

    def test_total_count_without_keyword(self):
        case_id = 1
        self.db_session.query.return_value.filter.return_value.count.return_value = 1
        result = self.session_repo.total_count(case_id)
        self.assertEqual(result, 1)
        self.db_session.close.assert_called_once()

    def test_get_list_with_keyword(self):
        case_id = 1
        skip = 0
        limit = 10
        keyword = "test"
        session_entities = [
            SessionEntity(
                id=1,
                name="test",
                session_state_id=1,
                case_id=1,
                source_video_url="/source/video.mp4",
                source_script_url="/source/script.json",
                script_state_id=1,
                analyze_state_id=1,
                created_date="2024-01-01",
                video_length="00:30:00",
                origin_video_url="/origin/video.mp4",
                encoding_video_url="/encoding/video.mp4",
            )
        ]
        sessions = [
            SessionDomain(
                id=1,
                name="test",
                session_state_id=1,
                case_id=1,
                source_video_url="/source/video.mp4",
                source_script_url="/source/script.json",
                script_state_id=1,
                analyze_state_id=1,
                created_date="2024-01-01",
                video_length="00:30:00",
                origin_video_url="/origin/video.mp4",
                encoding_video_url="/encoding/video.mp4",
            )
        ]
        self.db_session.query.return_value.filter.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = (
            session_entities
        )
        result = self.session_repo.get_list(case_id, skip, limit, keyword)
        self.assertEqual(result, sessions)
        self.db_session.close.assert_called_once()

    def test_get_list_without_keyword(self):
        case_id = 1
        skip = 0
        limit = 10
        session_entities = [
            SessionEntity(
                id=1,
                name="test",
                session_state_id=1,
                case_id=1,
                source_video_url="/source/video.mp4",
                source_script_url="/source/script.json",
                script_state_id=1,
                analyze_state_id=1,
                created_date="2024-01-01",
                video_length="00:30:00",
                origin_video_url="/origin/video.mp4",
                encoding_video_url="/encoding/video.mp4",
            )
        ]
        sessions = [
            SessionDomain(
                id=1,
                name="test",
                session_state_id=1,
                case_id=1,
                source_video_url="/source/video.mp4",
                source_script_url="/source/script.json",
                script_state_id=1,
                analyze_state_id=1,
                created_date="2024-01-01",
                video_length="00:30:00",
                origin_video_url="/origin/video.mp4",
                encoding_video_url="/encoding/video.mp4",
            )
        ]
        self.db_session.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = (
            session_entities
        )
        result = self.session_repo.get_list(case_id, skip, limit)
        self.assertEqual(result, sessions)
        self.db_session.close.assert_called_once()

    def test_list_by_state_id(self):
        state_id = 1
        session_entities = [
            SessionEntity(
                id=1,
                name="test",
                session_state_id=1,
                case_id=1,
                source_video_url="/source/video.mp4",
                source_script_url="/source/script.json",
                script_state_id=1,
                analyze_state_id=1,
                created_date="2024-01-01",
                video_length="00:30:00",
                origin_video_url="/origin/video.mp4",
                encoding_video_url="/encoding/video.mp4",
            )
        ]
        sessions = [
            SessionDomain(
                id=1,
                name="test",
                session_state_id=1,
                case_id=1,
                source_video_url="/source/video.mp4",
                source_script_url="/source/script.json",
                script_state_id=1,
                analyze_state_id=1,
                created_date="2024-01-01",
                video_length="00:30:00",
                origin_video_url="/origin/video.mp4",
                encoding_video_url="/encoding/video.mp4",
            )
        ]
        self.db_session.query.return_value.filter.return_value.all.return_value = (
            session_entities
        )
        result = self.session_repo.list_by_state_id(state_id)
        self.assertEqual(result, sessions)
        self.db_session.close.assert_called_once()

    def test_update_state_by_session_id_success(self):
        session_id = 1
        new_state_id = StateTypeEnum.START
        self.db_session.query.return_value.filter.return_value.update.return_value = 1
        res = self.session_repo.update_state_by_session_id(session_id, new_state_id)
        self.assertTrue(res)
        self.db_session.commit.assert_called_once()
        self.db_session.close.assert_called_once()

    def test_update_state_by_session_id_not_found(self):
        session_id = 1
        new_state_id = StateTypeEnum.START
        self.db_session.query.return_value.filter.return_value.update.return_value = 0
        res = self.session_repo.update_state_by_session_id(session_id, new_state_id)
        self.assertFalse(res)
        self.db_session.close.assert_called_once()

    def test_update_success(self):
        session_id = 1
        session = SessionDomain(
            id=1,
            name="updated_name",
            session_state_id=1,
            case_id=1,
            source_video_url="/source/video.mp4",
            source_script_url="/source/script.json",
            script_state_id=1,
            analyze_state_id=1,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="/origin/video.mp4",
            encoding_video_url="/encoding/video.mp4",
        )
        self.db_session.query.return_value.filter.return_value.update.return_value = 1
        res = self.session_repo.update(session_id, session)
        self.assertTrue(res)
        self.db_session.commit.assert_called_once()
        self.db_session.close.assert_called_once()

    def test_update_not_found(self):
        session_id = 1
        session = SessionDomain(
            id=1,
            name="updated_name",
            session_state_id=1,
            case_id=1,
            source_video_url="/source/video.mp4",
            source_script_url="/source/script.json",
            script_state_id=1,
            analyze_state_id=1,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="/origin/video.mp4",
            encoding_video_url="/encoding/video.mp4",
        )
        self.db_session.query.return_value.filter.return_value.update.return_value = 0
        res = self.session_repo.update(session_id, session)
        self.assertFalse(res)
        self.db_session.close.assert_called_once()

    def test_delete_success(self):
        session_id = 1
        self.db_session.query.return_value.filter.return_value.delete.return_value = 1
        res = self.session_repo.delete(session_id)
        self.assertTrue(res)
        self.db_session.commit.assert_called_once()
        self.db_session.close.assert_called_once()

    def test_delete_not_found(self):
        session_id = 1
        self.db_session.query.return_value.filter.return_value.delete.return_value = 0
        res = self.session_repo.delete(session_id)
        self.assertFalse(res)
        self.db_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
