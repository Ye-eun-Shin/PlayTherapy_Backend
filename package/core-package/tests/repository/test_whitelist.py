import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from core.repository.whitelist import WhitelistRepository
from core.model.domain.whitelist import WhiteList
from core.model.entity.whitelist import WhiteListEntity
from core.db.connection import ConnectionManager


class TestWhitelistRepository(unittest.TestCase):

    def setUp(self):
        self.connection_manager = MagicMock(spec=ConnectionManager)
        self.db_session = MagicMock(spec=Session)
        self.connection_manager.make_session.return_value = self.db_session
        self.whitelist_repo = WhitelistRepository(self.connection_manager)

    def test_get_whitelist_found(self):
        test_email = "test@example.com"
        whitelist_entity = WhiteListEntity(id=1, email="test@example.com")
        self.db_session.query.return_value.filter.return_value.first.return_value = (
            whitelist_entity
        )
        with patch(
            "core.model.domain.whitelist.WhiteList.model_validate",
            return_value=WhiteList(id=1, email="test@example.com"),
        ) as mock_model_validate:
            result = self.whitelist_repo.get(test_email)
            mock_model_validate.assert_called_once_with(whitelist_entity)
            self.assertIsNotNone(result)
            self.db_session.close.assert_called_once()

    def test_get_whitelist_not_found(self):
        test_email = "test@example.com"
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        result = self.whitelist_repo.get(test_email)
        self.assertIsNone(result)
        self.db_session.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
