from typing import Optional

from auth.exception import UserAlreadyExist, InvalidUserEmail
from core.model.domain.user import User
from core.repository.org import OrgRepository
from core.repository.user import UserRepository
from core.repository.whitelist import WhitelistRepository
from core.service.security import SecurityService
from core.db.connection import ConnectionManager
from core.db.transaction import transaction_scope


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        whitelist_repository: WhitelistRepository,
        org_repository: OrgRepository,
        security_service: SecurityService,
        connection_manager: ConnectionManager,
    ):
        self.user_repository = user_repository
        self.whitelist_repository = whitelist_repository
        self.org_repository = org_repository
        self.security_service = security_service
        self.connection_manager = connection_manager

    def add(self, user: User) -> User:
        session = self.connection_manager.make_session()
        with transaction_scope(session) as tx_session:
            whitelist = self.whitelist_repository.get(
                email=user.email, db_session=tx_session
            )
            if not whitelist:
                raise InvalidUserEmail(user.email)

            if self.user_repository.get_by_email(
                email=user.email, db_session=tx_session
            ):
                raise UserAlreadyExist(email=user.email)

            user.hashed_password = self.security_service.get_password_hash(
                user.hashed_password
            )
            user = self.user_repository.add(user=user, db_session=tx_session)

        return user

    def get_by_email(self, email: str) -> User:
        return self.user_repository.get_by_email(email=email)

    def get_by_email_and_password(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_email(email=email)

        if not user:
            return None

        if self.security_service.verify_password(password, user.hashed_password):
            return user
        else:
            return None