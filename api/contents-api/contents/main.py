import os
from fastapi import FastAPI
from dependency_injector import providers
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from core.exception import InvalidToken
from object.exception import UploadFailed, DownloadFailed
from contents.container import Container
from contents.setting.config import settings
from contents.exception import (
    CaseNotFound,
    SessionNotFound,
    VideoNotFound,
    ScriptNotFound,
    AnalyzeReportNotFound,
    InvalidRange,
)
from contents.route.case import router as case_router
from contents.route.session import router as session_router
from contents.route.video import router as video_router
from contents.route.script import router as script_router
from contents.route.analyze_report import router as analyze_report_router

container = Container()
container.config.from_yaml(f"./contents/config-{os.getenv('PHASE','LOCAL')}.yaml")

container.wire(packages=["contents.route"])
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://playtherapy-console.dsail.skku.edu",
    "playtherapy-argocd.dsail.skku.edu",
    "playtherapy-backend-alpha.dsail.skku.edu",
    "playtherapy-backend.dsail.skku.edu",
    "k8s-ingressn-ingressn-1653a1e369-42b18eda041d135d.elb.ap-northeast-2.amazonaws.com",
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(
    debug=True,
    title=settings.APP_TITLE,
    version=settings.VERSION,
    middleware=middleware,
)


@app.exception_handler(CaseNotFound)
async def case_not_found_handler(request: Request, exc: CaseNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(SessionNotFound)
async def session_not_found_handler(request: Request, exc: SessionNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(VideoNotFound)
async def video_not_found_handler(request: Request, exc: VideoNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(ScriptNotFound)
async def script_not_found_handler(request: Request, exc: ScriptNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(AnalyzeReportNotFound)
async def analyze_report_not_found_handler(
    request: Request, exc: AnalyzeReportNotFound
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(InvalidRange)
async def invalid_range_handler(request: Request, exc: InvalidRange):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(InvalidToken)
async def invalid_token_handler(request: Request, exc: InvalidToken):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(UploadFailed)
async def upload_failed_handler(request: Request, exc: UploadFailed):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(DownloadFailed)
async def download_failed_handler(request: Request, exc: DownloadFailed):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


def register_routers(app: FastAPI):
    app.include_router(case_router, prefix="/contents/api/case")
    app.include_router(session_router, prefix="/contents/api")
    app.include_router(video_router, prefix="/contents/api")
    app.include_router(script_router, prefix="/contents/api")
    app.include_router(analyze_report_router, prefix="/contents/api")


register_routers(app)
