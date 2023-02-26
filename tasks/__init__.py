from invoke import (
    Collection,
)
from invoke.main import program
from tasks import errno, tls, bucketfs, environment

namespace = Collection(errno, tls, bucketfs, environment)

if __name__ == "__main__":
    program.run()
