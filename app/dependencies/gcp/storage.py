from io import BytesIO
from typing import Any, List, Optional
from app.core.config import GCP_STORAGE_BUCKET_NAME
from google.cloud import storage


class GoogleCloudStorage:
    def __init__(self):
        self.__key_path: str = "./gcs_key.json"
        self.__client = storage.Client.from_service_account_json(self.__key_path)
        self.__bucket = self.__client.get_bucket(GCP_STORAGE_BUCKET_NAME)

    def key_path(self) -> str:
        return self.__key_path

    def bucket(self) -> storage.Bucket:
        return self.__bucket

    def client(self) -> storage.Client:
        return self.__client

    def ls(self) -> List[Any]:
        b_list = list(self.client().list_blobs(self.bucket()))
        print(b_list)
        return b_list

    def get_blob_by_name(self, file_path: str) -> Optional[storage.Blob]:
        return self.bucket().get_blob(file_path, self.client())

    @staticmethod
    def convert_blob_to_byte_string(file: storage.Blob):
        if file is not None:
            return BytesIO(file.download_as_string())
        else:
            return None
