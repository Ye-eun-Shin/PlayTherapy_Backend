import os
import io
from object.repository.analyze_report import AnalyzeReportRepository
from object.exception import UploadFailed, DownloadFailed
from core.model.domain.reports import AnalyzeReport


class AnalyzeReportService:
    def __init__(self, analyze_report_repository: AnalyzeReportRepository):
        self.analyze_report_repository = analyze_report_repository

    def upload(self, analyze_report: AnalyzeReport, file_path: str) -> str:
        try:
            key_count = self.analyze_report_repository.get_object_list(file_path)[
                "KeyCount"
            ]
            object_name = f"{file_path}/analyze_report_v{key_count+1}.json"

            data = analyze_report.model_dump_json().encode("utf-8")
            return self.analyze_report_repository.upload(data, object_name)
        except Exception as e:
            raise UploadFailed(file_path + "/analyze_report.json")
