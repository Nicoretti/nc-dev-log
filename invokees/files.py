"""Automation tasks for the crc project"""
from pathlib import Path

from typing import Iterable

from invoke import task

from invokees.terminal import stdout


def _python_files(
    project_root: Path, path_filters: Iterable[str] = ("dist", ".eggs", "venv")
) -> Iterable[Path]:
    """Returns all relevant"""
    return _deny_filter(project_root.glob("**/*.py"), deny_list=path_filters)


def _deny_filter(files: Iterable[Path], deny_list: Iterable[str]) -> Iterable[Path]:
    """
    Adds a filter to remove unwanted paths containing python files from the iterator.
     args:
     return:
    """
    for entry in deny_list:
        files = filter(lambda path: entry not in path.parts, files)
    return files


@task
def python(_context, root: str = "."):
    """
    List all python files within a specific root directory.

    Args:
        root: where the search shall be started (default: current working directory).
    """
    for f in _python_files(Path(root)):
        stdout.print(f)
