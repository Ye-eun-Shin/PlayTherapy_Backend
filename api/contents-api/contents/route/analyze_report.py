from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import StreamingResponse
from dependency_injector.wiring import inject, Provide

from contents.container import Container
from contents.service.analyze_report import AnalyzeReportManagerService
from core.service.security import SecurityService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/api/signin")


# 1. analyze_report(json) download
@router.get(
    "/case/{case_id}/session/{session_id}/analyze-report", tags=["analyze-report"]
)
@inject
async def download_analyze_report(
    case_id: int,
    session_id: int,
    token: str = Depends(oauth2_scheme),
    analyze_report_manager_service: AnalyzeReportManagerService = Depends(
        Provide[Container.analyze_report_manager_service]
    ),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    analyze_report = await analyze_report_manager_service.download_analyze_report(
        case_id=case_id, session_id=session_id, user_id=payload.get("user_id")
    )
    return StreamingResponse(analyze_report, media_type="application/json")
