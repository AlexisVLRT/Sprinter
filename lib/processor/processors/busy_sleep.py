import time
from random import random

from lib.processor.processors.base import BaseProcessor
from lib.misc.task import Task


class BusySleep(BaseProcessor):
    def __init__(self, task: Task):
        super().__init__(task=task)

    def run(self):
        sleep_time = random() * 30
        print(f"Busy sleeping for {sleep_time} secs")
        start = time.time()
        while time.time() - start < sleep_time:
            pass
