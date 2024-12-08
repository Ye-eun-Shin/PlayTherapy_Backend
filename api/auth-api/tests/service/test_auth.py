import unittest
from unittest.mock import AsyncMock, patch
import asyncio
from datetime import datetime
from fastapi.responses import JSONResponse

from auth.dto.auth import SigninRequest, AccessTokenResponse, SignupRequest
from auth.exception import UserNotFound
from core.model.domain.user import User
from core.exception import InvalidToken
from auth.service.user import UserService
from auth.service.auth import AuthService
from core.service.security import SecurityService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.user_service = AsyncMock(spec=UserService)
        self.security_service = AsyncMock(spec=SecurityService)
        self.auth_service = AuthService(
            user_service=self.user_service,
            security_service=self.security_service,
        )

    async def test_signup(self):
        signup_request = SignupRequest(
            email="test@example.com",
            name="test",
            hashed_password="test_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            user_type_id=1,
        )
        user = User(
            email="test@example.com",
            name="test",
            hashed_password="test_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=None,
        )
        user_domain = User(
            email="test@example.com",
            name="test",
            hashed_password="hashed_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        self.user_service.add.return_value = user_domain
        result = await self.auth_service.signup(signup_request)
        self.user_service.add.assert_called_once_with(user=user)
        self.assertEqual(result, user_domain)

    async def test_signin_success(self):
        signin_request = SigninRequest(
            email="test@example.com",
            password="test_password",
        )
        user = User(
            email="test@example.com",
            name="test",
            hashed_password="hashed_password",
            birth_year=2000,
            gender="N",
            highest_education_level_id=1,
            years_of_experience=1,
            created_time=datetime.now(),
            user_type_id=1,
            org_id=1,
        )
        self.user_service.get_by_email_and_password.return_value = user
        response = await self.auth_service.signin(signin_request)
        self.security_service.create_token.assert_called_once()
        self.assertIsInstance(response, AccessTokenResponse)

    async def test_signin_user_not_found(self):
        signin_request = SigninRequest(
            email="test@example.com",
            password="test_password",
        )
        self.user_service.get_by_email_and_password.return_value = None
        result = await self.auth_service.signin(signin_request)
        with self.assertRaises(UserNotFound):
            self.assertIsInstance(result, AccessTokenResponse)

    async def test_verify_token_success(self):
        access_token = "test_token"
        payload = {
            "user_email": "test@example.com",
            "user_name": "test",
            "user_type": 1,
        }
        self.security_service.decode_token.return_value = payload
        result = await self.auth_service.verify(access_token)
        self.assertEqual(result, payload)

    async def test_verify_token_invalid_token(self):
        access_token = "test_token"
        payload = {
            "user_id": 1,
            "user_email": "test@example.com",
            "user_name": "test",
            "user_type": 1,
        }
        self.security_service.decode_token.return_value = payload
        with self.assertRaises(InvalidToken):
            await self.auth_service.verify(access_token)

    async def test_refresh_token_success(self):
        access_token = "test_token"
        payload = {
            "user_id": 1,
            "user_email": "test@example.com",
            "user_name": "test",
            "user_type": 1,
        }
        self.auth_service.verify.return_value = payload
        result = await self.auth_service.refresh(access_token)
        self.security_service.create_token.assert_called_once_with(access_token)

    async def test_refresh_token_invalid_token(self):
        access_token = "test_token"
        with patch.object(
            self.auth_service, "verify", side_effect=InvalidToken(token=access_token)
        ):
            with self.assertRaises(InvalidToken):
                await self.auth_service.refresh(access_token)


if __name__ == "__main__":
    asyncio.run(unittest.main())
