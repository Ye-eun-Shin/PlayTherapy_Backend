import unittest
from unittest.mock import MagicMock
from boto3 import client
from object.storage.client import ClientManager
from object.repository.analyze_report import AnalyzeReportRepository


class TestAnalyzeReportRepository(unittest.TestCase):
    def setUp(self):
        self.client_manager = MagicMock(spec=ClientManager)
        self.analyze_report_repo = AnalyzeReportRepository(
            "bucket", self.client_manager
        )

    def test_upload(self):
        object_name = "object_name"
        data = b"some data"
        s3_client = MagicMock()
        self.client_manager.get_client.return_value = s3_client

        result = self.analyze_report_repo.upload(data, object_name)

        s3_client.put_object.assert_called_once_with(
            Bucket="bucket", Key="analyze_report/" + object_name, Body=data
        )
        self.assertEqual(result, object_name)

    def test_upload_exception(self):
        object_name = "object_name"
        data = b"some data"
        s3_client = MagicMock()
        s3_client.put_object.side_effect = Exception
        self.client_manager.get_client.return_value = s3_client

        result = self.analyze_report_repo.upload(data, object_name)

        s3_client.put_object.assert_called_once_with(
            Bucket="bucket", Key="analyze_report/" + object_name, Body=data
        )
        self.assertIsNone(result)

    def test_download(self):
        object_name = "object_name"
        s3_client = MagicMock()
        s3_client.get_object.return_value = {"Body": "file_content"}
        self.client_manager.get_client.return_value = s3_client

        result = self.analyze_report_repo.download(object_name)

        s3_client.get_object.assert_called_once_with(
            Bucket="bucket", Key="analyze_report/" + object_name
        )
        self.assertEqual(result, "file_content")

    def test_download_exception(self):
        object_name = "object_name"
        s3_client = MagicMock()
        s3_client.get_object.side_effect = Exception
        self.client_manager.get_client.return_value = s3_client

        result = self.analyze_report_repo.download(object_name)

        s3_client.get_object.assert_called_once_with(
            Bucket="bucket", Key="analyze_report/" + object_name
        )
        self.assertIsNone(result)

    def test_delete(self):
        object_name = "object_name"
        s3_client = MagicMock(spec=client("s3"))
        self.client_manager.get_client.return_value = s3_client
        result = self.analyze_report_repo.delete(object_name)
        s3_client.delete_object.assert_called_once_with(
            Bucket="bucket", Key="analyze_report/object_name"
        )
        self.assertEqual(result, object_name)

    def test_delete_exception(self):
        object_name = "object_name"
        s3_client = MagicMock(spec=client("s3"))
        s3_client.delete_object.side_effect = Exception
        self.client_manager.get_client.return_value = s3_client
        result = self.analyze_report_repo.delete(object_name)
        s3_client.delete_object.assert_called_once_with(
            Bucket="bucket", Key="analyze_report/object_name"
        )
        self.assertIsNone(result)

    def test_get_object_list(self):
        s3_client = MagicMock(spec=client("s3"))
        self.client_manager.get_client.return_value = s3_client
        s3_client.list_objects_v2.return_value = {"reports": [{"1-1": "report"}]}
        result = self.analyze_report_repo.get_object_list()
        self.assertEqual(result, {"reports": [{"1-1": "report"}]})

    def test_get_object_list_exception(self):
        s3_client = MagicMock(spec=client("s3"))
        s3_client.list_objects_v2.side_effect = Exception
        self.client_manager.get_client.return_value = s3_client
        result = self.analyze_report_repo.get_object_list()
        self.assertIsNone(result)
