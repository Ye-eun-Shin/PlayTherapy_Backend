import unittest
from unittest.mock import AsyncMock
import io
import os
from functools import wraps
from sqlalchemy.orm import Session
from object.repository.script import ScriptRepository
from object.exception import UploadFailed, DownloadFailed
from core.db.connection import ConnectionManager
from core.repository.session import SessionRepository
from core.repository.case import CaseRepository
from core.db.transaction import transaction_scope
from core.model.domain.session import Session as SessionDomain
from core.model.domain.state_type import StateTypeEnum
from contents.exception import CaseNotFound, SessionNotFound, ScriptNotFound
from contents.service.script import ScriptManagerService


class TestScriptService(unittest.TestCase):
    def SetUp(self):
        self.script_repository = AsyncMock(spec=ScriptRepository)
        self.session_repository = AsyncMock(spec=SessionRepository)
        self.case_repository = AsyncMock(spec=CaseRepository)
        self.connection_manager = AsyncMock(spec=ConnectionManager)
        self.db_session = AsyncMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.script_manager_service = ScriptManagerService(
            self.script_repository,
            self.session_repository,
            self.case_repository,
            self.connection_manager,
        )

    async def test_get_script_url_success(self):
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
        self.assertEqual(
            await self.script_manager_service.get_script_url(1), "1/1/script_v1.json"
        )

    async def test_get_script_url_not_found(self):
        self.session_repository.get.return_value = None
        with self.assertRaises(SessionNotFound):
            await self.script_manager_service.get_script_url(1)

    # 기존에 script_url이 있고, 새로운 script_url을 업로드하는 경우
    async def update_script_url_success(self):
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
        self.assertEqual(
            await self.script_manager_service.update_script_url(1, "1/1/script_v2.json"),
            "1/1/script_v2.json",
        )

    async def update_script_url_not_found(self):
        self.session_repository.get.return_value = None
        with self.assertRaises(SessionNotFound):
            await self.script_manager_service.update_script_url(1, "1/1/script_v2.json")

    async def download_script_success(self):
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
        script_body = io.BytesIO(b'{"script": "test"}')
        self.script_repository.get_json.return_value = script_body
        self.assertEqual(
            await self.script_manager_service.download_script(case_id, session_id, user_id),
            script_body,
        )

    async def download_script_not_found(self):
        self.session_repository.get.return_value = None
        with self.assertRaises(SessionNotFound):
            await self.script_manager_service.download_script(1, 1, 1)

    async def download_script_failed(self):
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
        self.script_repository.get_json.return_value = None
        with self.assertRaises(DownloadFailed):
            await self.script_manager_service.download_script(case_id, session_id, user_id)

    async def upload_script_success(self):
        case_id = 1
        session_id = 1
        user_id = 1
        script = b'{"script": "test"}'
        env = os.getenv("PHASE", "LOCAL")
        file_path = f"{env}/{case_id}/{session_id}"
        key_count = 0
        object_list = {"KeyCount": key_count}
        self.script_repository.get_object_list.return_value = object_list

        object_name = f"{file_path}/script_v{key_count+1}.json"
        self.script_repository.upload_json.return_value = object_name
        self.assertEqual(
            await self.script_manager_service.upload_script(
                script, user_id, case_id, session_id
            ),
            object_name,
        )

    async def upload_script_failed(self):
        case_id = 1
        session_id = 1
        user_id = 1
        script = b'{"script": "test"}'
        env = os.getenv("PHASE", "LOCAL")
        file_path = f"{env}/{case_id}/{session_id}"
        key_count = 0
        object_list = {"KeyCount": key_count}
        self.script_repository.get_object_list.return_value = object_list
        object_name = f"{file_path}/script_v{key_count+1}.json"
        self.script_repository.upload_json.return_value = None
        with self.assertRaises(UploadFailed):
            await self.script_manager_service.upload_script(
                script, user_id, case_id, session_id
            )
