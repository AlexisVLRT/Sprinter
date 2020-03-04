import base64
import json

import uuid as uuid

from lib.misc.task import Task
from lib.processor.processor_factory import ProcessorFactory

UUID = str(uuid.uuid4())


def main(event):
    enveloppe = event.get_json()
    task_json = json.loads(
        base64.b64decode(enveloppe["message"]["data"]).decode("utf8")
    )
    print(task_json)

    task = _build_task_object(task_json)

    task.update_attribute("container_instance", UUID)
    task.update_status("running")

    processor = ProcessorFactory(task.kwargs["processor_name"]).get_processor()(task)

    try:
        processor.run()
        task.update_status("done")
    except Exception:
        task.update_status("failed")

    return "OK"


def _build_task_object(task_json):
    return Task(
        task_id=task_json.pop("id"),
        status=task_json.pop("status"),
        start=task_json.pop("start"),
        **task_json,
    )
