import os

from dependency_injector import providers
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from auth.container import Container
from auth.exception import (
    UserAlreadyExist,
    UserNotFound,
    InvalidUserEmail,
)
from auth.setting.config import settings
from auth.route.auth import router as auth_router
from auth.route.config import router as config_router
from auth.route.user import router as user_router
from core.exception import InvalidToken

config = providers.Configuration()
container = Container()
container.config.from_yaml(f"./auth/config-{os.getenv('PHASE','LOCAL')}.yaml")

container.wire(packages=["auth.route"])

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


@app.exception_handler(UserAlreadyExist)
async def user_already_exist_handler(request: Request, exc: UserAlreadyExist):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(UserNotFound)
async def user_not_found_handler(request: Request, exc: UserNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.error_code},
    )


@app.exception_handler(InvalidUserEmail)
async def invalid_user_email_handler(request: Request, exc: InvalidUserEmail):
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


def register_routers(app: FastAPI):
    app.include_router(auth_router, prefix="/auth/api")
    app.include_router(user_router, prefix="/auth/api")
    app.include_router(
        config_router,
        prefix="/auth/api",
    )


register_routers(app)
