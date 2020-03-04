from google.cloud import pubsub_v1

import config
from lib.misc.singleton import Singleton


@Singleton
class Pubsub:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()

    def push_message(self, topic: str, message: str):
        topic_path = self.publisher.topic_path(config.PROJECT, topic)
        self.publisher.publish(topic_path, data=message.encode("utf-8"))
