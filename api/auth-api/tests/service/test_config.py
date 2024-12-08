import unittest
from unittest.mock import MagicMock, patch

from auth.dto.config import ConfigResponse
from core.model.domain.user import UserType
from core.model.domain.org import Org
from core.repository.org import OrgRepository
from core.repository.user import UserTypeRepository
from auth.service.config import ConfigService


class TestConfigService(unittest.TestCase):
    def setUp(self):
        self.user_type_repository = MagicMock(spec=UserTypeRepository)
        self.org_repository = MagicMock(spec=OrgRepository)
        self.config_service = ConfigService(
            user_type_repository=self.user_type_repository,
            org_repository=self.org_repository,
        )

    async def test_get_config(self):
        user_type = UserType(
            id=1,
            name="test",
        )
        org = Org(
            id=1,
            name="test",
        )
        user_types = [user_type, user_type]
        orgs = [org, org]
        self.user_type_repository.list.return_value = user_types
        self.org_repository.list.return_value = orgs
        result = await self.config_service.get()
        self.assertEqual(result, ConfigResponse(user_types=user_types, orgs=orgs))


if __name__ == "__main__":
    unittest.main()
