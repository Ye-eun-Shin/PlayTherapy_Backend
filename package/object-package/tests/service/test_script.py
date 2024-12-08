import unittest
from unittest.mock import MagicMock, patch
from object.service.script import ScriptService
from object.exception import UploadFailed, DownloadFailed


class TestScriptService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = ScriptService(self.mock_repo)

    def test_upload_script(self):
        self.mock_repo.get_object_list.return_value = {"KeyCount": 1}
        self.mock_repo.upload.return_value = "Success"

        result = self.service.upload_script("file_name", "file_path")

        self.mock_repo.get_object_list.assert_called_once_with("file_path")
        self.mock_repo.upload.assert_called_once_with(
            "file_name", "file_path/script_v2.json"
        )
        self.assertEqual(result, "Success")

    def test_download_script(self):
        mock_script_body = MagicMock()
        mock_script_body.read.return_value = "Script Content"
        self.mock_repo.get_json.return_value = mock_script_body

        result = self.service.download_script("file_path")

        self.mock_repo.get_json.assert_called_once_with("file_path")
        self.assertEqual(result, "Script Content")

    def test_get_script_list(self):
        self.mock_repo.get_object_list.return_value = {"KeyCount": 1}

        result = self.service.get_script_list("file_path")

        self.mock_repo.get_object_list.assert_called_once_with("file_path")
        self.assertEqual(result, {"KeyCount": 1})


if __name__ == "__main__":
    unittest.main()
