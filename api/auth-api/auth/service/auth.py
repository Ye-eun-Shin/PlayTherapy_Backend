from datetime import datetime
from fastapi.responses import JSONResponse

from auth.dto.auth import SigninRequest, AccessTokenResponse, SignupRequest
from auth.exception import UserNotFound
from core.model.domain.user import User
from auth.service.user import UserService
from core.model.domain.security import JwtPayload
from core.exception import InvalidToken
from core.service.security import SecurityService


class AuthService:
    def __init__(self, user_service: UserService, security_service: SecurityService):
        self.user_service = user_service
        self.security_service = security_service

    async def signup(self, signup_request: SignupRequest) -> User:
        user = User(id=None, created_time=datetime.now(), **signup_request.model_dump())
        result = self.user_service.add(user=user)

        return result

    async def signin(self, signin_request: SigninRequest) -> AccessTokenResponse:
        user = self.user_service.get_by_email_and_password(
            email=signin_request.email, password=signin_request.password
        )

        if user is None:
            raise UserNotFound(signin_request.email)

        access_token = self.security_service.create_token(
            data=JwtPayload(
                user_id=user.id,
                user_email=user.email,
                user_name=user.name,
                user_type=user.user_type_id,
            )
        )

        return AccessTokenResponse(access_token=access_token)

    async def verify(self, access_token: str) -> JwtPayload:
        try:
            payload = self.security_service.decode_token(access_token)
        except Exception as e:
            raise InvalidToken(token=access_token)

        if payload.get("user_id") is None:
            raise InvalidToken(token=access_token)

        return payload

    async def refresh(self, access_token: str) -> str:
        payload = await self.verify(access_token)

        if isinstance(payload, JSONResponse):
            raise InvalidToken(token=access_token)

        access_token = self.security_service.create_token(
            data=JwtPayload(
                user_id=payload.get("user_id"),
                user_email=payload.get("user_email"),
                user_name=payload.get("user_name"),
                user_type=payload.get("user_type"),
            )
        )
        return access_token
