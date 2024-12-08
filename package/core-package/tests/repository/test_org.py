import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from core.repository.org import OrgRepository
from core.model.domain.org import Org
from core.model.entity.org import OrgEntity
from core.db.connection import ConnectionManager


class TestOrgRepository(unittest.TestCase):

    def setUp(self):
        self.connection_manager = MagicMock(spec=ConnectionManager)
        self.db_session = MagicMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.org_repo = OrgRepository(self.connection_manager)

    def test_get_org_found(self):
        test_org_name = "test_org"
        org_entity = OrgEntity(
            id=1,
            name="test_org",
        )
        self.db_session.query.return_value.filter.return_value.first.return_value = (
            org_entity
        )
        result = self.org_repo.get(test_org_name)
        self.assertIsNotNone(result)
        self.db_session.close.assert_called_once()

    def test_get_org_not_found(self):
        test_org_name = "test_org"
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        result = self.org_repo.get(test_org_name)
        self.assertIsNone(result)
        self.db_session.close.assert_called_once()

    def test_list_org_non_empty(self):
        org_entity = OrgEntity(
            id=1,
            name="test_org",
        )
        org_entities = [org_entity, org_entity]
        self.db_session.query.return_value.all.return_value = org_entities
        result = self.org_repo.list()
        self.assertIsNotNone(result)
        self.db_session.close.assert_called_once()

    def test_list_org_empty(self):
        self.db_session.query.return_value.all.return_value = []
        result = self.org_repo.list()
        self.assertEqual(result, [])
        self.db_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
