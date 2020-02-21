import os
from pathlib import Path
from dotenv import load_dotenv
from subprocess import check_output


def env_vars_to_config_file():
    conf_path = Path(__file__).parent.parent / "config.py"

    with open(conf_path, "r") as file:
        lines = file.readlines()

    declarations = []
    for line in lines:
        if "=" in line:
            declarations.append(line.split("=")[0].strip())

    existing_vars = list(os.environ.keys())
    load_dotenv(dotenv_path=Path(".") / "environments" / os.getenv("ENV", "dev"))

    for env_var in os.environ:
        if env_var not in existing_vars and env_var not in declarations:
            lines.append(f"{env_var} = os.getenv('{env_var}')\n")

    with open(conf_path, "w") as out:
        out.writelines(lines)


def generate_reqs():
    check_output(["pip freeze > requirements.txt"], shell=True)


def black():
    check_output(["black . --exclude venv"], shell=True)


if __name__ == "__main__":
    env_vars_to_config_file()
    generate_reqs()
    black()
