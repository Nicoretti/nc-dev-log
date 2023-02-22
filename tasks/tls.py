from inspect import cleandoc
from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from contextlib import contextmanager
from invoke import task, Collection


def _check_for_openssl():
    if which("openssl"):
        return
    raise Exception("`openssl` is not available!")


_ROOT_KEY = "RootCA.key"
_ROOT_CERT = "RootCA.crt"
_DEFAULT_DESTINATION = "./certs"


@task
def ca(context, name="TestCA", destination=_DEFAULT_DESTINATION):
    """
    Create all artifacts required for a CA
    """
    _check_for_openssl()
    destination = Path(destination)
    destination.mkdir(exist_ok=True)

    keyfile = destination / _ROOT_KEY
    certificate = destination / _ROOT_CERT

    # create key pair for the CA
    context.run(f"openssl genrsa -aes256 -out {keyfile} 4096")
    # create the CA certificate
    subject = "/CN=TEST CA/C=DE/L=Bavaria/O=Test Organization"
    context.run(
        f"openssl req -x509 -new -nodes -key {keyfile} -sha256 -days 365 -out {certificate} -subj '{subject}'"
    )


_SAN_CONFIG_TEMPLATE = (
    cleandoc(
        """
    [req]
    default_bits  = 4096
    distinguished_name = req_distinguished_name
    req_extensions = req_ext
    x509_extensions = v3_req
    prompt = no
    [req_distinguished_name]
    countryName = XX
    stateOrProvinceName = N/A
    localityName = N/A
    organizationName = Self-signed certificate
    commonName = {name} 
    [req_ext]
    subjectAltName = @alt_names
    [v3_req]
    subjectAltName = @alt_names
    [alt_names]
    {dns_entries}
    {ip_entries}
"""
    )
    + "\n"
)


@contextmanager
def san_config(name, dns_entries=None, ip_entries=None):
    if not dns_entries and not ip_entries:
        raise Exception("At least one dns or ip entry must be specified")
    dns_entries = dns_entries if dns_entries else []
    ip_entries = ip_entries if ip_entries else []
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        config = tmpdir / "san.cnf"
        with open(config, "w") as f:
            f.write(
                _SAN_CONFIG_TEMPLATE.format(
                    name=name,
                    dns_entries="\n".join(
                        (f"DNS.{i} = {e}" for i, e in enumerate(dns_entries, 1))
                    ),
                    ip_entries="\n".join(
                        (f"IP.{i} = {e}" for i, e in enumerate(ip_entries, 1))
                    ),
                )
            )
        yield config


@task(iterable=["dns", "ip"])
def server(
    context,
    name="Test Server",
    destination=_DEFAULT_DESTINATION,
    dns=None,
    ip=None,
    root_cert=_ROOT_CERT,
    root_key=_ROOT_KEY,
):
    """
    Create all artifacts required for a server to do tls.
    """
    _check_for_openssl()
    destination = Path(destination)
    destination.mkdir(exist_ok=True)

    keyfile = destination / "Server.key"
    signing_request = destination / "Server.csr"
    certificate = destination / "Server.crt"

    # create a server key without password
    context.run(f"openssl genrsa -out {keyfile} 4096")

    with san_config(name, dns, ip) as config:
        # create singing request
        context.run(
            f"openssl req -new -sha256 -key {keyfile} -out {signing_request} -config {config} -extensions v3_req"
        )

        # create signed server certificate
        root_cert = Path(root_cert)
        root_key = Path(root_key)
        command = (
            f"openssl x509 -req -in {signing_request} -CA {root_cert} -CAkey {root_key} "
            f"-CAcreateserial -out {certificate} -days 90 -sha256 "
            f"-extfile {config} -extensions v3_req"
        )
        context.run(command)


namespace = Collection()
namespace.add_task(ca)
namespace.add_task(server)
