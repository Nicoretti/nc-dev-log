from collections import defaultdict
from invoke import task, Collection
from exasol.bucketfs import Service
from rich.tree import Tree
from rich.console import Console

_stdout = Console()
_stderr = Console(stderr=True)


@task
def buckets(_context, host="http://127.0.0.1", port=6666, username="w", password="write"):
    """
    List all buckets of a specific bucketfs service

    Args:
        host: (default: 'http://127.0.0.1')
        port: (default: 6666)
        username: (default: 'w')
        password: (default: 'write')
    """
    credentials = defaultdict(lambda: {"username": username, "password": password})
    bucketfs = Service(f"{host}:{port}", credentials)
    tree = Tree(f"🌐 Bucketfs", style="Red")
    try:
        for bucket in bucketfs:
            child = tree.add(f"💾 {bucket}", style="cyan")
            for f in bucketfs[bucket].files:
                child.add(f"📄 {f}", style="green")
    except Exception as ex:
        _stdout.print(f"Couldn't list bucket, details: {ex}")
    _stdout.print(tree)


namespace = Collection()
namespace.add_task(buckets)
