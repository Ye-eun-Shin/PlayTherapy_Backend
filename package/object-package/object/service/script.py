import io
from object.repository.script import ScriptRepository
from object.exception import UploadFailed, DownloadFailed


class ScriptService:
    def __init__(self, script_repository: ScriptRepository):
        self.script_repository = script_repository

    def upload_script(self, file_name: str, file_path: str):
        try:
            key_count = self.script_repository.get_object_list(file_path)["KeyCount"]

            object_name = f"{file_path}/script_v{key_count+1}.json"

            return self.script_repository.upload(file_name, object_name)
        except Exception as e:
            raise UploadFailed(file_name)

    def download_script(self, file_path: str):
        script_body = self.script_repository.get_json(file_path)
        if not script_body:
            raise DownloadFailed(file_path)
        return script_body.read()

    def get_script_list(self, file_path: str):
        try:
            return self.script_repository.get_object_list(file_path)
        except Exception as e:
            print(f"Cannot get script list in '{file_path}'. Error: {e}")
            return None
