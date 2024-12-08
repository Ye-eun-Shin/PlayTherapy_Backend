from object.storage.client import ClientManager


class AnalyzeReportRepository:
    def __init__(self, bucket: str, client_manager: ClientManager):
        self.bucket = bucket
        self.client_manager = client_manager
        self.path = "analyze_report/"

    def upload(self, data: bytes, object_name: str):
        try:
            client = self.client_manager.get_client()
            client.put_object(
                Bucket=self.bucket, Key=self.path + object_name, Body=data
            )
            return object_name
        except Exception as e:
            print(f"Cannot upload json: '{object_name}' to S3. Error: {e}")
            return None

    def download(self, object_name: str):
        try:
            client = self.client_manager.get_client()
            response = client.get_object(
                Bucket=self.bucket, Key=self.path + object_name
            )
            return response["Body"]
        except Exception as e:
            print(f"Cannot download file: '{object_name}' from S3.")
            return None

    def delete(self, object_name: str):
        try:
            client = self.client_manager.get_client()
            client.delete_object(Bucket=self.bucket, Key=self.path + object_name)
            return object_name
        except Exception as e:
            print(f"Cannot delete file: '{object_name}' from S3.")
            return None

    def get_object_list(self, file_path: str = ""):
        try:
            client = self.client_manager.get_client()
            return client.list_objects_v2(
                Bucket=self.bucket, Prefix=self.path + file_path
            )
        except Exception as e:
            print(f"Cannot get object list in '{self.path}' from S3.")
            return None
