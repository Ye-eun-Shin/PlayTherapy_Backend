from abc import ABC
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from core.model.domain.security import Token, JwtPayload
from core.exception import InvalidToken


class SecurityService(ABC):

    def __init__(self, secret_key: str, algorithm: str, expires_delta: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_delta = expires_delta
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_token(self, data: JwtPayload):
        if self.expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=self.expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)

        payload = {
            "user_id": data.user_id,
            "user_email": data.user_email,
            "user_name": data.user_name,
            "user_type": data.user_type,
            "iat": datetime.utcnow(),
            "exp": expire,
        }

        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str):
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def verify_token(self, token: str):
        try:
            payload = self.decode_token(token)
        except Exception as e:
            raise InvalidToken(token=token)
        if payload.get("user_id") is None:
            raise InvalidToken(token=token)
        return payload

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)
