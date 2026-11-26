"""Simple local deployment for the Jenkins pipeline.

Copies app.py into a release folder outside the Jenkins workspace (the
workspace is wiped by cleanWs after every build), keeps one folder per build,
updates a 'current' folder, then runs the deployed copy to check it works.
"""
import os
import runpy
import shutil
import sys
from datetime import datetime

FILES = ["app.py", "requirements.txt"]


def deploy(target_root, build_number):
    release_name = f"build-{build_number}"
    release_dir = os.path.join(target_root, "releases", release_name)
    current_dir = os.path.join(target_root, "current")
    os.makedirs(release_dir, exist_ok=True)

    for name in FILES:
        shutil.copy2(name, release_dir)

    with open(os.path.join(release_dir, "VERSION.txt"), "w") as f:
        f.write(f"build {build_number}\n")
        f.write(f"deployed at {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    if os.path.isdir(current_dir):
        shutil.rmtree(current_dir)
    shutil.copytree(release_dir, current_dir)
    return current_dir


def smoke_test(current_dir):
    """Run the deployed app.py and check that it greets correctly."""
    sys.path.insert(0, current_dir)
    try:
        module = runpy.run_path(os.path.join(current_dir, "app.py"))
    finally:
        sys.path.pop(0)
    message = module["greet"]("World")
    if message != "Hello, World from Karim Zarzour!":
        raise SystemExit(f"Smoke test failed: got {message!r}")
    return message


def main():
    target_root = os.environ.get(
        "DEPLOY_DIR",
        os.path.join(os.path.expanduser("~"), "jenkins_project_deploy"),
    )
    build_number = os.environ.get("BUILD_NUMBER", "local")

    current_dir = deploy(target_root, build_number)
    message = smoke_test(current_dir)

    print(f"Deployed build {build_number} to {current_dir}")
    print(f"Smoke test output: {message}")


if __name__ == "__main__":
    main()
