import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn
import click

from lib.misc.job import Job


@click.command()
@click.option("--job-id")
def monitor_job(job_id: str):
    job = Job(job_id=job_id)

    start = time.time()
    report_hist = []
    seaborn.set()
    _, axes = plt.subplots(1, 1)

    while 1:
        timer = time.time()
        report = _get_report(job)
        print(report)
        report_hist.append(
            {
                "queued": report["queued"],
                "running": report["running"],
                "done": report["done"],
            }
        )
        axes.clear()
        pd.DataFrame(report_hist).plot(ax=axes)
        plt.pause(0.0001)
        if report["done"] == report["total"] != 0:
            job.update_status("done")
            report_hist[-1]["update_time"] = time.time() - timer
            break

        time.sleep(max(0, 1 - (time.time() - timer)))
        report_hist[-1]["update_time"] = time.time() - timer

    sum_running = sum([report["running"] for report in report_hist])
    print(sum_running, "cpu.second")
    print(sum_running * 0.00000463)
    print(
        f"Done in {time.time() - start}, avg per task: {(time.time() - start) / report['total']}"
    )
    plt.show()


def _get_report(job: Job):
    tasks = [task for task in job.get_tasks()]
    running = [task for task in tasks if task.status == "running"]
    n_pending = len([task for task in tasks if task.status == "pending"])
    n_queued = len([task for task in tasks if task.status == "queued"])
    n_done = len([task for task in tasks if task.status == "done"])
    n_running = len(
        {
            task.kwargs["container_instance"]
            for task in running
            if "container_instance" in task.kwargs
        }
    )
    return {
        "pending": n_pending,
        "queued": n_queued,
        "running": n_running,
        "done": n_done,
        "total": n_pending + n_queued + n_running + n_done,
    }


if __name__ == "__main__":
    monitor_job()
