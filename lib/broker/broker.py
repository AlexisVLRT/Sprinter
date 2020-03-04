import json
import os
import logging
import time
import traceback


from lib.cloud_utils.pubsub import Pubsub
from bottle import Bottle, HTTPResponse
import config
from lib.misc.job import Job

app = Bottle()


@app.route("/run/<job_id>")
def run(job_id):
    job = Job(job_id=job_id)
    job.update_status("running")
    logging.info(f"Starting new job with id {job.id}")

    try:
        _broker_tasks(job)
    except Exception:
        logging.error(traceback.format_exc())
        return HTTPResponse(
            status=500, body=json.dumps({"payload": traceback.format_exc()})
        )

    logging.info(f"Job queue for {job.id} distributed")
    return HTTPResponse(
        status=200, body=f"Tasks brokering done. Distributed {len(job.tasks)} tasks"
    )


def _broker_tasks(job: Job):
    all_tasks, tasks, empty_slots = _get_tasks(job)
    while any(tasks):
        start = time.time()
        selected_tasks = []
        for _ in range(min(empty_slots, len(tasks))):
            task = tasks.pop(0)
            selected_tasks.append(task)

        job.batch_update_tasks(selected_tasks, "status", "queued")
        for task in selected_tasks:
            Pubsub.instance().push_message(
                config.BROKER_TOPIC, task.json(),
            )
        print(time.time() - start)

        all_tasks, tasks, empty_slots = _get_tasks(job)


def _get_tasks(job: Job):
    all_tasks = job.get_tasks_with_status("pending")
    tasks = [task for task in all_tasks]
    empty_slots = (
        int(config.MAX_CONCURRENT_TASKS)
        - job.count_tasks_with_status("queued", update_tasks=False)
        - job.count_tasks_with_status("running", update_tasks=False)
    )
    return all_tasks, tasks, empty_slots


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
