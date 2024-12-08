import unittest
from unittest.mock import AsyncMock
import io
from object.repository.analyze_report import AnalyzeReportRepository
from object.exception import DownloadFailed
from core.repository.session import SessionRepository
from core.repository.case import CaseRepository
from core.model.domain.session import Session as SessionDomain
from core.model.domain.state_type import StateTypeEnum
from core.db.connection import ConnectionManager
from contents.exception import CaseNotFound, SessionNotFound, AnalyzeReportNotFound
from sqlalchemy.orm import Session
from contents.service.analyze_report import AnalyzeReportManagerService


class TestAnalyzeReportManagerService(unittest.TestCase):
    def SetUp(self):
        self.analyze_report_repository = AsyncMock(spec=AnalyzeReportRepository)
        self.session_repository = AsyncMock(spec=SessionRepository)
        self.case_repository = AsyncMock(spec=CaseRepository)
        self.connection_manager = AsyncMock(spec=ConnectionManager)
        self.db_session = AsyncMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.analyze_report_manager_service = AnalyzeReportManagerService(
            self.analyze_report_repository,
            self.session_repository,
            self.case_repository,
        )

    async def test_get_analyze_report_url_success(self):
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
            analyze_url="1/1/analyze_report_v1.json",
        )
        self.session_repository.get.return_value = session
        self.assertEqual(
            await self.analyze_report_manager_service.get_analyze_report_url(1),
            "1/1/analyze_report_v1.json",
        )

    async def test_get_analyze_report_url_not_found(self):
        self.session_repository.get.return_value = None
        with self.assertRaises(SessionNotFound):
            await self.analyze_report_manager_service.get_analyze_report_url(1)

    async def test_download_analyze_report_success(self):
        self.analyze_report_manager_service.get_analyze_report_url = (
            "1/1/analyze_report_v1.json"
        )
        self.analyze_report_repository.download.return_value = io.BytesIO(b"test")
        self.assertEqual(
            await self.analyze_report_manager_service.download_analyze_report(1, 1, 1),
            io.BytesIO(b"test"),
        )

    async def test_download_analyze_report_not_found(self):
        self.analyze_report_manager_service.get_analyze_report_url = None
        with self.assertRaises(AnalyzeReportNotFound):
            await self.analyze_report_manager_service.download_analyze_report(1, 1, 1)
