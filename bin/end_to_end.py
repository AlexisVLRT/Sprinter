import time
from subprocess import check_output

from lib.misc.task import Task
from lib.misc.job import Job
import config


def new_job(n_tasks: int = 1) -> Job:
    job = Job()
    print(job.id)

    print("Creating tasks")
    start = time.time()
    for _ in range(n_tasks):
        task = Task(job.id, new_entity=True, processor_name="busy_sleep")
        job.add_task(task)

    print(f"Done in {time.time() - start}")

    print("Posting job")
    start = time.time()
    job.post()
    print(f"Done in {time.time() - start}")
    return job


def start_processing(job: Job):
    print(f"curl -X get {config.BROKER_ENDPOINT}/run/{job.id}")
    print(
        check_output([f"curl -X get {config.BROKER_ENDPOINT}/run/{job.id}"], shell=True)
    )


if __name__ == "__main__":
    job = new_job(1)
    time.sleep(1)
    start_processing(job)
