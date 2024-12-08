from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide

from auth.service.auth import AuthService
from auth.service.user import UserService
from auth.container import Container

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/api/signin")


@router.get("/user", tags=["GetUser"])
@inject
async def get_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    payload = await auth_service.verify(token)
    user = user_service.get_by_email(email=payload["user_email"])
    user.hashed_password = ""
    return user
