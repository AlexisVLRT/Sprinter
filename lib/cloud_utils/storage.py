from google.cloud import storage
import config


def load_to_gcs(filename: str, data: str) -> None:
    client = storage.Client()
    bucket = client.get_bucket(config.DATA_BUCKET)
    blob = bucket.blob(config.INPUT_PATH + "/" + filename)
    blob.upload_from_string(data)
