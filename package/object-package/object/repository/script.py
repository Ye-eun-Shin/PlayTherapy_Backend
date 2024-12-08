from object.storage.client import ClientManager


class ScriptRepository:
    def __init__(self, bucket: str, client_manager: ClientManager):
        self.bucket = bucket
        self.client_manager = client_manager
        self.path = "script/"

    def upload(self, file_name: str, object_name: str):
        try:
            client = self.client_manager.get_client()
            client.upload_file(file_name, self.bucket, self.path + object_name)
            return object_name
        except Exception as e:
            print(f"Cannot upload file: '{object_name}' to S3. Error: {e}")
            return None

    def upload_json(self, json_data: bytes, object_name: str):
        try:
            client = self.client_manager.get_client()
            client.put_object(
                Bucket=self.bucket, Key=self.path + object_name, Body=json_data
            )
            return object_name
        except Exception as e:
            print(f"Cannot upload json: '{object_name}' to S3. Error: {e}")
            return None

    def download(self, object_name: str, file_name: str):
        try:
            client = self.client_manager.get_client()
            client.download_file(self.bucket, self.path + object_name, file_name)
            return object_name
        except Exception as e:
            print(f"Cannot download file: '{object_name}' from S3.")
            return None

    def get_json(self, object_name: str):
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
