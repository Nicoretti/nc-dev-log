from invoke import (
    Collection,
)
from invoke.main import program
from tasks import (
    errno,
    tls,
    bucketfs
)

namespace = Collection(
    errno,
    tls,
    bucketfs
)

if __name__ == "__main__":
    program.run()
