from uuid import uuid4
import inspect

from lib.cloud_utils.datastore import Datastore


class BaseJob:
    def __init__(self):
        self.id = str(uuid4())
        self.status = "pending"
        self.datastore = Datastore.instance()
        self.datastore_entity = None

    def post(self):
        if self.datastore_entity is None:
            self.datastore_entity = self.datastore.create_entity(
                kind=self.__class__.__name__, entity_id=self.id, **self.to_dict()
            )
        self.datastore.post_entities(entities=[self.datastore_entity])

    def update_status(self, status: str):
        self.status = status
        self.update_attribute("status", status)

    def update_attribute(self, key, value):
        new_attr = {key: value}
        self.datastore.update_entities(
            entities=[self.datastore_entity], new_attributes=new_attr
        )

    def to_dict(self):
        members = inspect.getmembers(
            self, lambda member: not (inspect.isroutine(member))
        )
        attrs = {
            attr: value
            for attr, value in members
            if not attr.startswith("__")
            and not attr.endswith("__")
            and attr != "kwargs"
            and attr != "datastore"
            and attr != "datastore_entity"
        }
        return attrs
