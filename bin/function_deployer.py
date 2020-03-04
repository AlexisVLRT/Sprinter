from pathlib import Path
import shutil

from lib.cloud_utils.functions import Functions


def deploy(entrypoint_file: Path):
    package_dir = Path(__file__).parent.parent / "_func_deployment_package"
    build_deployment_package(package_dir / entrypoint_file, package_dir)
    Functions().deploy(package_dir)
    clean_deployment_dir(package_dir)


def build_deployment_package(entrypoint_file: Path, deployment_dir: Path):
    make_minimal_gcloudignore()
    init_deployment_dir(deployment_dir)

    for path in _get_paths_to_copy():
        if path.is_file():
            shutil.copy2(path, deployment_dir)
        else:
            shutil.copytree(path, deployment_dir / path.stem, dirs_exist_ok=True)

    move_entrypoint_to_root(entrypoint_file, deployment_dir)


def move_entrypoint_to_root(entrypoint_file: Path, package_dir: Path):
    shutil.copy2(str(entrypoint_file), str(package_dir / "main.py"))


def init_deployment_dir(deployment_dir: Path):
    clean_deployment_dir(deployment_dir)
    deployment_dir.mkdir(parents=True, exist_ok=True)


def clean_deployment_dir(deployment_dir: Path):
    shutil.rmtree(str(deployment_dir), ignore_errors=True)


def make_minimal_gcloudignore():
    if not _gcloudignore_exists():
        with open(Path(__file__).parent.parent / ".gcloudignore", "r") as gcloudignore:
            gcloudignore.writelines(["_func_deployment_package"])


def _get_paths_to_copy() -> set:
    return set(Path(__file__).parent.parent.iterdir()) - _get_paths_not_to_copy()


def _get_paths_not_to_copy() -> set:
    if not _gcloudignore_exists():
        return set()

    lines = set()
    root_dir = Path(__file__).parent.parent
    with open(root_dir / ".gcloudignore", "r") as gcloudignore:
        for line in gcloudignore.readlines():
            if len(line.strip()) and not line.startswith("#"):
                path = root_dir / line.strip()
                lines.update({path})
    return lines


def _gcloudignore_exists() -> bool:
    return (Path(__file__).parent.parent / ".gcloudignore").exists()


if __name__ == "__main__":
    print(deploy(Path("lib/processor/entrypoint.py")))
