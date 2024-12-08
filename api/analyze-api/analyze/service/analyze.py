import json
import os
import datetime
import traceback
import threading
from object.service.script import ScriptService
from object.service.analyze_report import AnalyzeReportService
from core.repository.session import SessionRepository
from core.db.connection import ConnectionManager
from core.model.domain.state_type import StateTypeEnum
from core.model.domain.session import Session
from core.model.domain.reports import AnalyzeReport
from core.model.domain.script import Script
from core.model.domain.reports import BatchPromptReport
from core.db.transaction import transaction_scope
from analyze.service.observation import ObservationService
from analyze.service.langflow_service import LangflowService
from analyze.utils.script_util import make_merged_script


class AnalyzeService:
    CHAT_INPUT_KEY = "ChatInput-XebAY"
    TEXT_INPUT_KEY = "TextInput-VTqI0"

    def __init__(
        self,
        connection_manager: ConnectionManager,
        script_service: ScriptService,
        analyze_report_service: AnalyzeReportService,
        session_repository: SessionRepository,
        langflow_service: LangflowService,
        observation_service: ObservationService,
    ):
        self.connection_manager = connection_manager
        self.script_service = script_service
        self.analyze_report_service = analyze_report_service
        self.session_repository = session_repository
        self.langflow_service = langflow_service
        self.observation_service = observation_service

    def to_clean_dict(self, report_dict: dict):
        # 최상위 JSON에서 message 값 추출
        try:
            raw_message = report_dict["outputs"][0]["outputs"][0]["messages"][0][
                "message"
            ]
        except:
            return {"reports": -1}

        # '```json'과 '```'을 제거하여 JSON 부분만 추출
        clean_message = raw_message.replace("```json", "").replace("```", "").strip()

        return json.loads(clean_message)

    def export(self, analyze_report: AnalyzeReport, session_id: int):
        env = os.getenv("PHASE", "LOCAL")
        file_path = f"{env}/{session_id}"
        file_name = self.analyze_report_service.upload(analyze_report, file_path)
        return file_name

    def run(self, script_url):
        """
        1. script_url을 받아서 script download
        2. observation에서 관찰척도 리스트 가져오기
        3. 관찰척도 리스트에 대해 iterate하며 langflow_service.run() 호출
        4. json dict -> BatchPromptReport 변환
        5. BatchPromptReport를 합쳐서 AnalyzeReport 생성
        """
        script_body = self.script_service.download_script(script_url)
        scripts = Script(**json.loads(script_body.decode("utf-8")))
        script = make_merged_script(scripts)

        observations = self.observation_service.list()

        analyze_report = dict()
        for obs in observations:
            print(f"[AnalyzeService] observations: {obs.kor_name}")
            input_dict = {
                self.CHAT_INPUT_KEY: {
                    "input_value": script,
                },
                self.TEXT_INPUT_KEY: {"input_value": obs.kor_name},
            }
            langflow_res = self.to_clean_dict(
                self.langflow_service.run(obs.kor_name, input_dict)
            )["reports"]

            # reports가 제대로 나오지 않은 경우
            if not isinstance(langflow_res, dict):
                print(f"[AnalyzeService] result error in '{obs.kor_name}'")
                langflow_res = {
                    "descriptions": "",
                    "interactions": [],
                    "level": langflow_res,
                }
            elif langflow_res["level"] is None:
                print(f"[AnalyzeService] result error in '{obs.kor_name}'")
                langflow_res["level"] = -1

            if "interactions" in langflow_res.keys() and not isinstance(
                langflow_res["interactions"], list
            ):
                langflow_res["interactions"] = [langflow_res["interactions"]]

            langflow_res["category"] = obs.eng_name
            report = BatchPromptReport(**langflow_res)
            analyze_report[obs.eng_name] = report

        return AnalyzeReport(reports=analyze_report)

    def run_from_db(self):
        """
        1. session 중 READY 상태인 것을 찾아 script_url을 가져온다.
        2. run() 호출하여 AnalyzeReport 생성
        3. run()에서 생성된 AnalyzeReport를 s3에 upload
        4. 분석 완료 후 DONE 상태로 변경
        """
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        print(f"[AnalyzeService] run from db at {formatted_time}")

        target_session: Session = None
        update_analyze_start_state = False
        update_analyze_done_state = False
        try:
            db_session = self.connection_manager.make_session()
            with transaction_scope(db_session) as tx_session:
                target_session: Session = (
                    self.session_repository.get_by_analyze_state_id(
                        state_id=StateTypeEnum.READY, db_session=db_session
                    )
                )
                if target_session is None:
                    print(f"[AnalyzeService] no target_session")
                    return

                if (
                    target_session.source_script_url is None
                    or target_session.source_script_url == ""
                ):
                    print(
                        f"[AnalyzeService] session id:[{target_session.id}] no target_session"
                    )
                    return

                print(
                    f"[AnalyzeService] session_id:[{target_session.id}] update target session state"
                )
                update_analyze_start_state = (
                    self.session_repository.update_analyze_state_by_session_id(
                        session_id=target_session.id,
                        new_state_id=int(StateTypeEnum.START),
                        db_session=tx_session,
                    )
                )

            script_path = target_session.source_script_url
            print(
                f"[AnalyzeService] session_id:[{target_session.id}] start analyze script {script_path}"
            )
            analyze_report = self.run(script_path)

            file_name = self.export(analyze_report, target_session.id)
            db_session = self.connection_manager.make_session()
            with transaction_scope(db_session) as tx_session:
                print(
                    f"[AnalyzeService] session_id:[{target_session.id}] upload analyze file {file_name}"
                )
                target_session.analyze_url = file_name
                target_session.analyze_state_id = int(StateTypeEnum.DONE)
                update_analyze_done_state = self.session_repository.update(
                    session_id=target_session.id,
                    session=target_session,
                    db_session=tx_session,
                )

        except Exception as e:
            print(traceback.format_exc())
            if update_analyze_start_state or update_analyze_done_state:
                db_session = self.connection_manager.make_session()
                with transaction_scope(db_session) as tx_session:
                    self.session_repository.update_analyze_state_by_session_id(
                        session_id=target_session.id,
                        new_state_id=int(StateTypeEnum.ERROR),
                        db_session=tx_session,
                    )
