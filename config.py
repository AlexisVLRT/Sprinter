import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import logging


load_dotenv(dotenv_path=Path(".") / "environments" / os.getenv("ENV", "dev"))

client = logging.Client()
client.setup_logging(log_level=10)  # 10 is DEBUG, 20 is INFO

PROJECT = os.getenv("PROJECT")
REGION = os.getenv("REGION")
DATA_BUCKET = os.getenv("DATA_BUCKET")
INPUT_PATH = os.getenv("INPUT_PATH")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")
SERVICE_ACCOUNT_ID = os.getenv("SERVICE_ACCOUNT_ID")
SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT")
SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_JSON")
PORT = os.getenv("PORT")
BROKER_TOPIC = os.getenv("BROKER_TOPIC")
BROKER_SUB = os.getenv("BROKER_SUB")
PROCESSOR_PATH = os.getenv("PROCESSOR_PATH")
PROCESSOR_SERVICE = os.getenv("PROCESSOR_SERVICE")
PROCESSOR_CONTAINER_TAG = os.getenv("PROCESSOR_CONTAINER_TAG")
PROCESSOR_CONTAINER = os.getenv("PROCESSOR_CONTAINER")
PROCESSOR_GCR_PATH = os.getenv("PROCESSOR_GCR_PATH")
