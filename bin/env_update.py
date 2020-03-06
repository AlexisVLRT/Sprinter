from subprocess import run, PIPE
from pathlib import Path

import click


@click.command()
@click.option("--update-type")
def update_env(update_type: str):
    if update_type == "init":
        new_values = get_conf()
    elif update_type == "broker_endpoint":
        new_values = get_broker_endpoint()
    else:
        raise ValueError("Arg must be either 'init' or 'broker_endpoint'")
    write_env(new_values)


def write_env(new_values: str):
    env_vals = get_env()
    env_vals.update(new_values)
    env_vals = [f"{key}={value}\n" for key, value in env_vals.items()]

    with open(Path(__file__).parent.parent / "environments/dev", "w") as env:
        env.writelines(env_vals)


def get_broker_endpoint():
    res = run(
        [f"gcloud run services list --platform=managed --region={get_env()['REGION']}"],
        shell=True,
        stdout=PIPE,
    )
    data = res.stdout.decode("utf-8").strip().split("\n")
    for line in data[1:]:
        words = [word for word in line.split(" ") if word]
        if words[1] == get_env()["BROKER_SERVICE"]:
            return {"BROKER_ENDPOINT": words[3]}
    raise ValueError("Broker cloud run not deployed")


def get_env():
    with open(Path(__file__).parent.parent / "environments/dev", "r") as env:
        return {
            line.split("=")[0]: line.strip().split("=")[1]
            for line in env.readlines()
            if line.strip()
        }


def get_conf() -> dict:
    values = {
        "PROJECT": "project",
        "REGION": "compute/region",
    }
    for name, value in values.items():
        values[name] = get_value(value)
    return values


def get_value(value) -> str:
    res = run([f"gcloud config get-value {value}"], shell=True, stdout=PIPE)
    return res.stdout.decode("utf-8").strip()


if __name__ == "__main__":
    update_env()
