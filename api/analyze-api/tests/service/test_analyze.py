import warnings

warnings.filterwarnings("ignore")
import json
import os
import unittest
from analyze.container import Container
from datetime import datetime


class TestAnalyzeService(unittest.TestCase):

    def setUp(self):
        self.container = Container()
        self.container.config.from_yaml("tests\config-TEST.yaml")
        self.container.wire(packages=["tests"])
        self.analyze_service = self.container.analyze_service()

    def test_run(self):
        # print(self.analyze_service.run("test/test.json"))

        analyze_report_obj = self.analyze_service.run("test/test_script2.json")
        analyze_report_dict = analyze_report_obj.model_dump()
        print(analyze_report_dict)

        file_name = (
            f"test_results/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        os.makedirs("test_results", exist_ok=True)
        with open(file_name, "w", encoding="utf8") as f:
            json.dump(analyze_report_dict, f, ensure_ascii=False, indent=4)

        print(f"\n\n>>>>>>>>>>>\n\nFINISH!!!!!!!!!!!!!")
