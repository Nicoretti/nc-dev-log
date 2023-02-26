from invoke import (
    Collection,
)
from invoke.main import program
from tasks import errno, tls, bucketfs, environment, code, files

namespace = Collection(errno, tls, bucketfs, environment, code, files)

if __name__ == "__main__":
    program.run()
