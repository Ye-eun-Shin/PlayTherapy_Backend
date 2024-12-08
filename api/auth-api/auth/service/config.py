from auth.dto.config import ConfigResponse
from core.repository.org import OrgRepository
from core.repository.user import UserTypeRepository


class ConfigService:
    def __init__(
        self, user_type_repository: UserTypeRepository, org_repository: OrgRepository
    ):
        self.user_type_repository = user_type_repository
        self.org_repository = org_repository

    async def get(self) -> ConfigResponse:
        user_types = self.user_type_repository.list()
        orgs = self.org_repository.list()

        return ConfigResponse(user_types=user_types, orgs=orgs)
