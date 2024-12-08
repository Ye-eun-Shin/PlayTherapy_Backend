import warnings

warnings.filterwarnings("ignore")

import unittest
from analyze.container import Container
import json


class TestLangflowService(unittest.TestCase):

    def setUp(self):
        self.container = Container()
        self.container.config.from_yaml("tests/config-TEST.yaml")
        self.container.wire(packages=["tests"])
        self.langflow_service = self.container.langflow_service()

    def test_run(self):
        res = self.langflow_service.run(
            input_value="test", input_dict={"input": "dict"}
        )

        # 최상위 JSON에서 message 값 추출
        raw_message = res["outputs"][0]["outputs"][0]["messages"][0]["message"]

        # '```json'과 '```'을 제거하여 JSON 부분만 추출
        clean_message = raw_message.replace("```json", "").replace("```", "").strip()

        # JSON 파싱
        parsed_data = json.loads(clean_message)
        print("\n\n>>>>>>>>>>>\n\n", parsed_data)
