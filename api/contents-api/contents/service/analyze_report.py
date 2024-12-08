import io
from functools import wraps
from object.repository.analyze_report import AnalyzeReportRepository
from object.exception import DownloadFailed
from core.repository.session import SessionRepository
from core.repository.case import CaseRepository
from contents.exception import CaseNotFound, SessionNotFound, AnalyzeReportNotFound


class AnalyzeReportManagerService:
    def __init__(
        self,
        analyze_report_repository: AnalyzeReportRepository,
        session_repository: SessionRepository,
        case_repository: CaseRepository,
    ):
        self.analyze_report_repository = analyze_report_repository
        self.session_repository = session_repository
        self.case_repository = case_repository

    def check_case_exists(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            case_id = kwargs.get("case_id")
            user_id = kwargs.get("user_id")
            case = self.case_repository.get(case_id=case_id, user_id=user_id)
            if not case:
                raise CaseNotFound(case_id)
            return await func(self, *args, **kwargs)

        return wrapper

    async def get_analyze_report_url(self, session_id):
        session = self.session_repository.get(session_id)
        if not session:
            raise SessionNotFound(session_id)
        return session.analyze_url

    @check_case_exists
    async def download_analyze_report(
        self, case_id: int, session_id: int, user_id: int
    ):
        analyze_report_url = await self.get_analyze_report_url(session_id)
        if not analyze_report_url:
            raise AnalyzeReportNotFound(session_id)

        analyze_report_body = self.analyze_report_repository.download(
            analyze_report_url
        )
        if not analyze_report_body:
            raise DownloadFailed(analyze_report_url)
        return io.BytesIO(analyze_report_body.read())
