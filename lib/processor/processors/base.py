from abc import ABC
from lib.misc.task import Task


class BaseProcessor(ABC):
    def __init__(self, task: Task):
        self.task = task

    def run(self):
        raise NotImplementedError
