from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth.dto.auth import SigninRequest, SignupRequest
from core.model.domain.user import User
from auth.service.auth import AuthService
from auth.container import Container

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/api/signin")


# 회원가입 API
@router.post("/signup", tags=["SignUp"])
@inject
async def signup(
    signup_request: SignupRequest,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),

) -> User:
    user = await auth_service.signup(signup_request=signup_request)
    user.hashed_password = ""

    return user


# Signin API
@router.post("/signin", tags=["Signin"])
@inject
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    user_name = form_data.username
    password = form_data.password
    signin_request = SigninRequest(email=user_name, password=password)
    access_token = await auth_service.signin(signin_request=signin_request)
    return access_token


# jwt 토큰 검증 API
@router.post("/verify", tags=["Verify"])
@inject
async def verify(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    payload = await auth_service.verify(access_token=token)
    return payload


# jwt 토큰 갱신 API
@router.post("/refresh", response_model=str, tags=["Refresh"])
@inject
async def refresh(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    access_token = await auth_service.refresh(access_token=token)

    return access_token
