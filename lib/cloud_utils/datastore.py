import logging
import time
from typing import List

from google.cloud import datastore

from lib.misc.singleton import Singleton


@Singleton
class Datastore:
    def __init__(self):
        self._client = datastore.Client()

    def get_tasks_entities_of_job(self, job_id: str) -> List[datastore.Entity]:
        return self._get_entities(kind="Task", filter={"job_id": job_id})

    def update_entities(self, entities: List[datastore.Entity], new_attributes: dict):
        for entity in entities:
            for key, value in new_attributes.items():
                entity[key] = value

        with self._client.transaction():
            self.post_entities(entities)

    def post_entities(self, entities: List[datastore.Entity]):
        for i in range(0, len(entities), 500):
            logging.info(f"Posting {len(entities[i: i + 500])} entities")
            batch = self._client.batch()
            batch.begin()
            [batch.put(entity) for entity in entities[i : i + 500]]
            batch.commit()

    def create_entity(self, kind: str, entity_id: str, **kwargs) -> datastore.Entity:
        key = self._client.key(kind)
        entity = datastore.Entity(key)
        entity.update(dict({"id": entity_id, "start": time.time()}, **kwargs))
        return entity

    def find_entity_from_id(
        self, entity_type: str, entity_id: str
    ) -> datastore.entity.Entity:
        query = self._client.query(kind=entity_type)
        query.add_filter("id", "=", entity_id)

        result = list(query.fetch())
        if not len(result):
            raise Exception("Entity is not in datastore")

        return result[0]

    def delete_job(self, job_id: str):
        self.delete_entities(kind="Job", filter={"id": job_id})
        self.delete_entities(kind="Task", filter={"job_id": job_id})

    def delete_entities(self, kind: str, filter: dict):
        entities = self._get_entities(kind=kind, filter=filter)

        keys = [entity.key for entity in entities]
        logging.info(f"Deleting {len(keys)} entities from the datastore")
        for i in range(0, len(keys), 500):
            batch = self._client.batch()
            batch.begin()
            [batch.delete(key) for key in keys[i : i + 500]]
            batch.commit()

    def _get_entities(self, kind: str, filter: dict) -> List[datastore.Entity]:
        query = self._client.query(kind=kind)

        for key, value in filter.items():
            query.add_filter(key, "=", value)

        return list(query.fetch())
