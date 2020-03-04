from lib.misc.basejob import BaseJob
from lib.misc.task import Task


class Job(BaseJob):
    def __init__(self, job_id=None):
        super().__init__()
        self.tasks = []

        if job_id is not None:
            self.id = job_id
            self.datastore_entity = self.datastore.find_entity_from_id(
                entity_type=self.__class__.__name__, entity_id=job_id
            )
            self._get_tasks_from_datastore()
        else:
            job_dct = self.to_dict()
            del job_dct["tasks"]
            self.datastore_entity = self.datastore.create_entity(
                kind="Job", entity_id=self.id, **job_dct
            )

    def post(self):
        task_entities = [task.datastore_entity for task in self.tasks]
        self.datastore.post_entities(task_entities)

        self.datastore.post_entities(entities=[self.datastore_entity])

    def add_task(self, task):
        self.tasks.append(task)

    def count_tasks_with_status(self, status: str, update_tasks=True) -> int:
        return len(self.get_tasks_with_status(status, update_tasks))

    def get_tasks(self, update_tasks=True) -> list:
        if update_tasks:
            self._update_tasks()
        return [task for task in self.tasks]

    def batch_update_tasks(self, tasks, key: str, value):
        task_entities = [task.datastore_entity for task in tasks]
        self.datastore.update_entities(task_entities, {key: value})

    def get_tasks_with_status(self, status: str, update_tasks=True) -> list:
        if update_tasks:
            self._update_tasks()

        tasks = [task for task in self.tasks if task.status == status]
        return tasks

    def delete_from_datastore(self):
        self.datastore.delete_job(self.id)

    def _update_tasks(self):
        self.tasks = []
        self._get_tasks_from_datastore()

    def _get_tasks_from_datastore(self):
        for task in self.datastore.get_tasks_entities_of_job(self.id):
            task_dict = dict(task)
            task_object = Task(
                task_id=task_dict.pop("id"),
                status=task_dict.pop("status"),
                start=task_dict.pop("start"),
                datastore_entity=task,
                **task_dict
            )
            task_object.datastore_entity = task
            self.tasks.append(task_object)
