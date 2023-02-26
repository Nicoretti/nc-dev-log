from pathlib import Path
from invoke import task, Collection
from tasks.files import _python_files

from rich.console import Console
from tasks.cmd import command

_stdout = Console()
_stderr = Console(stderr=True)


@task(
    name="format",
    aliases=["fmt"],
)
def format(context, root: str = ".", fix: bool = True, color: bool = True):
    """
    Run code formatter(s)

    Args:
       root: default .
       fix:
    """
    root = Path(root)
    files = _python_files(root)
    context.run(command("black", *files), pty=color)


@task
def lint(context, root: str = ".", fix=True, color=True):
    """Run linting"""
    root = Path(root)
    files = _python_files(root)
    context.run(command("ruff", *files), pty=color)


namespace = Collection()
namespace.add_task(format)
namespace.add_task(lint)
