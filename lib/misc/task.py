import json

from lib.misc.basejob import BaseJob


class Task(BaseJob):
    def __init__(
        self,
        job_id,
        task_id=None,
        datastore_entity=None,
        status=None,
        start=None,
        new_entity=False,
        **kwargs
    ):
        super().__init__()
        self.job_id = job_id

        if task_id is not None:
            self.id = task_id
        if status is not None:
            self.status = status
        if start is not None:
            self.start = start
        if datastore_entity is not None:
            self.datastore_entity = datastore_entity

        self.kwargs = kwargs

        if self.datastore_entity is None:
            in_datastore = False
            if not new_entity:
                try:
                    self.get_entity()
                    in_datastore = True
                except Exception as e:
                    print("Entity is not in datastore")
                    if e.args[0] != "Entity is not in datastore":
                        raise
            if not in_datastore:
                self.datastore_entity = self.datastore.create_entity(
                    kind=self.__class__.__name__, entity_id=self.id, **self.to_dict()
                )

    def get_entity(self):
        self.datastore_entity = self.datastore.find_entity_from_id(
            entity_type=self.__class__.__name__, entity_id=self.id
        )

    def to_dict(self):
        return dict(super().to_dict(), **self.kwargs)

    def json(self):
        return json.dumps(self.to_dict())
