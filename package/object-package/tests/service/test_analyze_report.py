import unittest
import io
from unittest.mock import MagicMock, patch
from core.model.domain.reports import AnalyzeReport
from object.service.analyze_report import AnalyzeReportService
from object.repository.analyze_report import AnalyzeReportRepository
from object.exception import UploadFailed, DownloadFailed


class TestAnalyzeReportService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock(spec=AnalyzeReportRepository)
        self.service = AnalyzeReportService(self.mock_repo)

    def test_upload_anlyze_report(self):
        analyze_report = AnalyzeReport(reports={"1-1": {}})
        file_path = "test"
        self.mock_repo.get_object_list.return_value = {"KeyCount": 0}
        self.mock_repo.upload.return_value = file_path + "/analyze_report_v1.json"

        result = self.service.upload(analyze_report, file_path)

        self.mock_repo.get_object_list.assert_called_once_with(file_path)
        self.mock_repo.upload.assert_called_once_with(
            analyze_report.model_dump_json().encode("utf-8"),
            file_path + "/analyze_report_v1.json",
        )
        self.assertEqual(result, file_path + "/analyze_report_v1.json")


if __name__ == "__main__":
    unittest.main()
