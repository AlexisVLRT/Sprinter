from typing import List

from google.cloud import storage

from lib.misc.singleton import Singleton
import config


@Singleton
class Storage:
    def __init__(self):
        self._client = storage.Client()

    def to_gcs(self, bucket: str, filepath: str, data: str) -> None:
        bucket = self._client.get_bucket(bucket)
        blob = bucket.blob(filepath)
        blob.upload_from_string(data)

    def from_gcs(self, bucket: str, filepath: str) -> List[str]:
        bucket = self._client.get_bucket(bucket)
        blobs = bucket.list_blobs(prefix=filepath)
        return [blob.download_as_string().decode("utf8") for blob in blobs]
