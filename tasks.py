from invoke import (
    Collection,
)
from invoke.main import program
from invokees import files
from invokees import code
from invokees import bucketfs
from invokees import environment
from invokees import errno
from invokees import tls

namespace = Collection(errno, tls, bucketfs, environment, code, files)

if __name__ == "__main__":
    program.run()
