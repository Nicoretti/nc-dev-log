import os
from collections import Counter

from invoke import (
    Collection,
    task,
)
from rich.table import Table
from rich.console import Console
from rich.theme import Theme

themes = Theme({
    "info": "cyan",
    "warning": "yellow",
    "danger": "bold red"
})

_stdout = Console(theme=themes)
_stderr = Console(theme=themes, stderr=True)


@task
def env(_context, table=True):
    def raw(e):
        for name, value in e.items():
            yield f"{name}: {value}"

    def table_based(e):
        table = Table(title="Environment Variables", highlight=True)
        table.add_column("Name", justify="left")
        table.add_column("Value")
        for name, value in e.items():
            table.add_row(f"{name}", value)
        yield table

    output = table_based if table else raw
    for e in output(os.environ):
        _stdout.print(e)


@task
def path(_context, warnings=True):
    paths = os.environ['PATH'].split(':')
    duplicates = (p for p, count in Counter(paths).items() if count > 1) if warnings else []
    for p in duplicates:
        _stderr.print(f"Warning: found duplicates of {p} in PATH", style='warning')
    deduplicated_paths = dict().fromkeys(paths)
    for p in deduplicated_paths:
        _stdout.print(p)


namespace = Collection('env')
namespace.add_task(env)
namespace.add_task(path)
