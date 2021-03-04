"""Setup script"""

import os
import subprocess

from types import FunctionType
from typing import List, TextIO
from setuptools import find_packages, setup

from mendeley_watchdog.cli import mendeley

HEREDIR = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS_TXT = "requirements.txt"

PROG = "mendeley-watchdog"
DESC = "Distributes Mendeley bibtex file to specific destination upon change"
VERSION = "0.0.1c01"

def get_entrypoint(name: str, function: FunctionType) -> str:
    """Get setuptools entrypoint with name for function"""
    return "{}={}:{}".format(
        name, function.__module__, function.__name__
    )


def open_local(filename: str, mode: str = "r") -> TextIO:
    """Open file in this directory."""

    return open(os.path.join(HEREDIR, filename), mode)


def execute_command(args: List[str]) -> List[str]:
    """Execute external command and return stdout"""

    try:
        process = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        return [line.strip() for line in process.stdout.splitlines()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def create_requirements_txt() -> None:
    """Create file 'requirements.txt' from 'Pipfile.lock'."""

    try:
        with open_local("Pipfile.lock"):
            pass
    except FileNotFoundError:
        return

    pipenv_lines = execute_command(["pipenv", "lock", "-r"])
    if not pipenv_lines:
        return

    reqs = [line for line in pipenv_lines[1:] if line]
    with open_local(REQUIREMENTS_TXT, "w") as req_file:
        req_file.write("\n".join(reqs) + "\n")


def read_requirements() -> List[str]:
    """Read lines of requirements.txt and return them as list"""

    with open_local(REQUIREMENTS_TXT) as req_file:
        return [
            line.strip() for line in req_file.readlines()
            if line.strip() and not line.startswith("-i")
        ]


if __name__ == '__main__':
    create_requirements_txt()
    README = open_local("README.md").read()
    REQUIREMENTS = read_requirements()
    INSTALL_REQUIRES = REQUIREMENTS if REQUIREMENTS else None
    setup(
        name=PROG,
        description=DESC,
        version=VERSION,
        long_description=README,
        install_requires=INSTALL_REQUIRES,
        packages=find_packages(),
        include_package_data=True,
        entry_points={"console_scripts": [
            get_entrypoint(mendeley.NAME, mendeley.main)
        ]})
