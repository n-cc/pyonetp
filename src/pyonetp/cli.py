"""CLI."""

import io
import os
import secrets
import sys
import typing

import click

from pyonetp.exceptions import EmptyKeyError
from pyonetp.exceptions import KeyLengthError
from pyonetp.operations import decrypt as decrypt_data
from pyonetp.operations import encrypt as encrypt_data


def _write(
    func: typing.Callable[..., bytes],
    out: str,
    keys: list[io.BufferedReader],
    allow_input_wrapping: bool,
) -> None:
    f: io.BufferedWriter | typing.BinaryIO = sys.stdout.buffer

    if out:
        f = open(out, "wb")

    try:
        f.write(
            func(*[k.read() for k in keys], allow_input_wrapping=allow_input_wrapping)
        )
    except KeyLengthError as e:
        click.echo(
            f"Input #{e.idx + 1} is shorter than the primary input, refusing to continue.\nRun with --allow-input-wrapping to allow keys to be wrapped (doing so is insecure).",
            err=True,
        )
        sys.exit(1)
    except EmptyKeyError as e:
        click.echo(
            f"Input #{e.idx + 1} is empty, refusing to continue.",
            err=True,
        )
        sys.exit(1)


@click.group()
def cli() -> None:
    """Encrypt and decrypt one time pads."""
    pass


@click.command()
@click.argument("inputs", nargs=-1, required=True)
@click.option("--out", help="Write encrypted data to specified file (default: stdout)")
@click.option(
    "--genkey",
    help="Generate a key to use for encryption and write it to the specified path. Uses secrets.SystemRandom.randbytes, which should be reasonably secure on most platforms; if in doubt,\
    generate your own keys.",
    multiple=True,
)
@click.option(
    "--allow-input-wrapping",
    help="Allow non-primary files (keys) to be wrapped if they are shorter than the primary file (data). This is inherently insecure and must be toggled manually.",
    is_flag=True,
)
def encrypt(
    inputs: tuple[str], out: str, genkey: tuple[str], allow_input_wrapping: bool
) -> None:
    """Encrypt files.

    Accepts an arbitrary number of files as input. The first file is generally the data to be encrypted, and the remaining files are the encryption keys, though this is not required.
    """
    keys = [open(i, "rb") for i in inputs]

    pk_len = len(keys[0].read())
    keys[0].seek(os.SEEK_SET)

    for gk in genkey:
        with open(gk, "wb") as k:
            k.write(secrets.SystemRandom().randbytes(pk_len))
        keys.append(open(gk, "rb"))

    _write(encrypt_data, out, keys, allow_input_wrapping)


cli.add_command(encrypt)


@click.command()
@click.argument("inputs", nargs=-1, required=True)
@click.option("--out", help="Write decrypted data to specified file (default: stdout)")
@click.option(
    "--allow-input-wrapping",
    help="Allow non-primary input files (keys) to be wrapped if they are shorter than the primary file (data). Only needed if this option was required and set during encryption.",
    is_flag=True,
)
def decrypt(inputs: tuple[str], out: str, allow_input_wrapping: bool) -> None:
    """Decrypt files.

    Accepts an arbitrary number of files as input. The first file is generally the file to be decrypted, and the remaining files are the encryption keys, though this is not required.
    The non-primary files must should be at least as long as the primary file.
    """
    keys = [open(i, "rb") for i in inputs]
    _write(decrypt_data, out, keys, allow_input_wrapping)


cli.add_command(decrypt)
