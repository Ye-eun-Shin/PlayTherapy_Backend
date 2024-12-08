import http
import json

import requests
import logging
import http.client as http_client
import subprocess


class LangflowService:
    def __init__(self, langflow_host: str, langflow_token: str, flow_id: str):
        self.langflow_token = langflow_token
        self.langflow_host = langflow_host
        self.flow_id = flow_id

        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    """
    def run(self, input_value: str, input_dict: dict) -> str:
        url = f"{self.langflow_host}/api/v1/run/{self.flow_id}?stream=false"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": f"{self.langflow_token}",
        }
        data = {
            "message": input_value,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": input_dict,
        }

        conn = http.client.HTTPConnection("playtherapy-langflow-alpha.dsail.skku.edu")

        try:
            conn.request(
                "POST",
                f"/api/v1/run/{self.flow_id}?stream=false",
                body=json.dumps(data),
                headers=headers,
            )

            response = conn.getresponse()

            print("Status Code:", response.status)
            response_data = response.read().decode()
            print("Response JSON:", response_data)

            response_json = json.loads(response_data)
            print("Parsed JSON:", response_json)
            return response_json
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            return None

    """

    def run(self, input_value: str, input_dict: dict) -> dict:
        langflow_host = self.langflow_host
        flow_id = self.flow_id
        langflow_token = self.langflow_token

        url = f"http://{langflow_host}/api/v1/run/{flow_id}?stream=false"
        headers = {"Content-Type": "application/json", "x-api-key": langflow_token}
        data = {
            "message": input_value,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": input_dict,
        }

        curl_command = [
            "curl",
            "-s",
            "-X",
            "POST",
            url,
            "-H",
            f"Content-Type: {headers['Content-Type']}",
            "-H",
            f"x-api-key: {headers['x-api-key']}",
            "-d",
            "@-",  # stdin으로 데이터를 전달
        ]

        try:
            # Popen을 사용하여 데이터를 파이프를 통해 전달
            process = subprocess.Popen(
                curl_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )

            # stdin을 통해 JSON 데이터를 전달
            stdout, stderr = process.communicate(input=json.dumps(data))

            # 명령어 실행 결과 출력
            print("Status Code:", process.returncode)
            print("Response JSON:", stdout)

            response_json = json.loads(stdout)
            print("Parsed JSON:", response_json)
            return response_json
        except Exception as e:
            print(f"An error occurred: {e}")
