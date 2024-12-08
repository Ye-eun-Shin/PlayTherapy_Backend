import unittest
from unittest.mock import AsyncMock
import os
from functools import wraps
from typing import IO
from sqlalchemy.orm import Session
from object.repository.video import VideoRepository
from object.exception import UploadFailed, DownloadFailed
from core.db.connection import ConnectionManager
from core.repository.session import SessionRepository
from core.repository.case import CaseRepository
from core.model.domain.session import Session as SessionDomain
from core.model.domain.state_type import StateTypeEnum
from contents.exception import CaseNotFound, SessionNotFound, VideoNotFound
from contents.service.video import VideoManagerService


class TestVideoManageService(unittest.TestCase):
    def setUp(self):
        self.video_repository = AsyncMock(spec=VideoRepository)
        self.session_repository = AsyncMock(spec=SessionRepository)
        self.case_repository = AsyncMock(spec=CaseRepository)
        self.connection_manager = AsyncMock(spec=ConnectionManager)
        self.db_session = AsyncMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.video_manager_service = VideoManagerService(
            self.video_repository,
            self.session_repository,
            self.case_repository,
            self.connection_manager,
        )

    # script까지 올려진 상태라고 가정
    async def test_get_encoded_video_url_success(self):
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
            await self.video_manager_service.get_encoded_video_url(1), "1/1/encoded_video.mp4"
        )

    async def test_get_encoded_video_url_not_found(self):
        self.session_repository.get.return_value = None
        with self.assertRaises(SessionNotFound):
            await self.video_manager_service.get_encoded_video_url(1)

    # 처음 video upload하는 경우라고 가정
    async def test_update_origin_video_url_success(self):
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=StateTypeEnum.READY,
            case_id=1,
            source_video_url="video.mp4",
            source_script_url=None,
            script_state_id=StateTypeEnum.NONE,
            analyze_state_id=StateTypeEnum.NONE,
            encoding_state_id=StateTypeEnum.NONE,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url=None,
            encoding_video_url=None,
        )
        self.session_repository.get.return_value = session
        self.session_repository.update.return_value = True
        self.assertEqual(
            await self.video_manager_service.update_origin_video_url(1, "1/1/video.mp4"),
            "1/1/video.mp4",
        )

    async def test_update_origin_video_url_not_found(self):
        self.session_repository.get.return_value = None
        with self.assertRaises(SessionNotFound):
            await self.video_manager_service.update_origin_video_url(1, "1/1/video.mp4")

    # encoded video까지 올려진 상태여야 함. script는 아직 생성되지 않았다고 가정
    async def test_download_video_success(self):
        case_id = 1
        session_id = 1
        user_id = 1
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=StateTypeEnum.READY,
            case_id=1,
            source_video_url="video.mp4",
            source_script_url=None,
            script_state_id=StateTypeEnum.NONE,
            analyze_state_id=StateTypeEnum.NONE,
            encoding_state_id=StateTypeEnum.DONE,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="1/1/video.mp4",
            encoding_video_url="1/1/encoded_video.mp4",
        )
        self.session_repository.get.return_value = session
        self.video_repository.get_object.return_value = {"Body": "video"}
        self.assertEqual(
            await self.video_manager_service.download_video(case_id, session_id, user_id),
            "video",
        )

    # encoded video url이 없는 경우
    async def test_download_video_not_found(self):
        case_id = 1
        session_id = 1
        user_id = 1
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=StateTypeEnum.READY,
            case_id=1,
            source_video_url="video.mp4",
            source_script_url=None,
            script_state_id=StateTypeEnum.NONE,
            analyze_state_id=StateTypeEnum.NONE,
            encoding_state_id=StateTypeEnum.NONE,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="1/1/video.mp4",
            encoding_video_url=None,
        )
        self.session_repository.get.return_value = session
        with self.assertRaises(VideoNotFound):
            await self.video_manager_service.download_video(case_id, session_id, user_id)

    # video를 s3에서 찾을 수 경우
    async def test_download_video_failed(self):
        case_id = 1
        session_id = 1
        user_id = 1
        session = SessionDomain(
            id=1,
            name="test",
            session_state_id=StateTypeEnum.READY,
            case_id=1,
            source_video_url="video.mp4",
            source_script_url=None,
            script_state_id=StateTypeEnum.NONE,
            analyze_state_id=StateTypeEnum.NONE,
            encoding_state_id=StateTypeEnum.DONE,
            created_date="2024-01-01",
            video_length="00:30:00",
            origin_video_url="1/1/video.mp4",
            encoding_video_url="1/1/encoded_video.mp4",
        )
        self.session_repository.get.return_value = session
        self.video_repository.get_object.return_value = None
        with self.assertRaises(DownloadFailed):
            await self.video_manager_service.download_video(case_id, session_id, user_id)

    # video upload 성공
    async def test_upload_video_obj_success(self):
        case_id = 1
        session_id = 1
        user_id = 1
        file_obj = AsyncMock(spec=IO)
        filename = "video.mp4"
        env = os.getenv("PHASE", "LOCAL")
        file_path = f"{env}/{case_id}/{session_id}/"
        self.video_repository.upload_obj.return_value = file_path + filename
        self.update_origin_video_url.return_value = "1/1/video.mp4"
        self.assertEqual(
            await self.video_manager_service.upload_video_obj(
                case_id, session_id, user_id, file_obj, filename
            ),
            file_path + filename,
        )

    async def test_upload_video_obj_failed(self):
        case_id = 1
        session_id = 1
        user_id = 1
        file_obj = AsyncMock(spec=IO)
        filename = "video.mp4"
        self.video_repository.upload_obj.return_value = None
        with self.assertRaises(UploadFailed):
            await self.video_manager_service.upload_video_obj(
                case_id, session_id, user_id, file_obj, filename
            )
