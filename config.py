import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import logging


load_dotenv(dotenv_path=Path(".") / "environments" / os.getenv("ENV", "dev"))

client = logging.Client()
client.setup_logging(log_level=20)  # 10 is DEBUG, 20 is INFO

PROJECT = os.getenv("PROJECT")
REGION = os.getenv("REGION")
PORT = os.getenv("PORT")
DATA_BUCKET = os.getenv("DATA_BUCKET")
INPUT_PATH = os.getenv("INPUT_PATH")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")
SERVICE_ACCOUNT_ID = os.getenv("SERVICE_ACCOUNT_ID")
SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT")
SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_JSON")
TASKS_BUFFER_TOPIC = os.getenv("TASKS_BUFFER_TOPIC")
TASKS_BUFFER_SUB = os.getenv("TASKS_BUFFER_SUB")
BROKER_TOPIC = os.getenv("BROKER_TOPIC")
BROKER_SUB = os.getenv("BROKER_SUB")
BROKER_SERVICE = os.getenv("BROKER_SERVICE")
BROKER_CONTAINER_TAG = os.getenv("BROKER_CONTAINER_TAG")
BROKER_CONTAINER = os.getenv("BROKER_CONTAINER")
BROKER_GCR_PATH = os.getenv("BROKER_GCR_PATH")
BROKER_ENDPOINT = os.getenv("BROKER_ENDPOINT")
PROCESSOR_SERVICE = os.getenv("PROCESSOR_SERVICE")
PROCESSOR_CONTAINER_TAG = os.getenv("PROCESSOR_CONTAINER_TAG")
PROCESSOR_CONTAINER = os.getenv("PROCESSOR_CONTAINER")
PROCESSOR_GCR_PATH = os.getenv("PROCESSOR_GCR_PATH")
PROCESSOR_ENDPOINT = os.getenv("PROCESSOR_ENDPOINT")
MAX_CONCURRENT_TASKS = os.getenv("MAX_CONCURRENT_TASKS")
BROKER_MEMORY = os.getenv("BROKER_MEMORY")
PROCESSOR_MEMORY = os.getenv("PROCESSOR_MEMORY")
