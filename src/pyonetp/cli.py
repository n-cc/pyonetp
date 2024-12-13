"""CLI."""

import io
import os
import sys
import typing

import click

from pyonetp.operations import decrypt as decrypt_data
from pyonetp.operations import encrypt as encrypt_data


@click.group()
def cli() -> None:
    """Encrypt and decrypt one time pads."""
    pass


@click.command()
@click.argument("inputs", nargs=-1, required=True)
@click.option("--out", help="Write encrypted data to specified file (default: stdout)")
@click.option(
    "--genkey",
    help="Generate a key to use for encryption and write it to the specified path",
    multiple=True,
)
def encrypt(inputs: tuple[str], out: str, genkey: tuple[str]) -> None:
    """Encrypt files.

    Accepts an arbitrary number of files as input. The first file is generally the data to be encrypted, and the remaining files are the encryption keys, though this is not required.
    The non-primary files must be at least as long as the primary file.
    """
    p_len = open(inputs[0]).seek(0, os.SEEK_END)

    for i in inputs[1:]:  # type: str
        if open(i).seek(0, os.SEEK_END) < p_len:
            click.echo(
                f"Non-primary input {i} is shorter than primary input {inputs[0]}, refusing to continue.",
                err=True,
            )
            sys.exit(1)

    for kf in genkey:
        with open(kf, "wb") as fk:
            fk.write(os.urandom(p_len))

    f: io.BufferedWriter | typing.BinaryIO = sys.stdout.buffer

    if out:
        f = open(out, "wb")

    f.write(encrypt_data(*[open(f, "rb").read() for f in inputs + genkey]))


cli.add_command(encrypt)


@click.command()
@click.argument("inputs", nargs=-1, required=True)
@click.option("--out", help="Write decrypted data to specified file (default: stdout)")
def decrypt(inputs: tuple[str], out: str) -> None:
    """Decrypt files.

    Accepts an arbitrary number of files as input. The first file is generally the file to be decrypted, and the remaining files are the encryption keys, though this is not required.
    The non-primary files must should be at least as long as the primary file.
    """
    p_len = open(inputs[0]).seek(0, os.SEEK_END)

    for i in inputs[1:]:  # type: str
        if open(i).seek(0, os.SEEK_END) < p_len:
            click.echo(
                f"Non-primary input {i} is shorter than primary input {inputs[0]}, refusing to continue.",
                err=True,
            )
            sys.exit(1)

    f: io.BufferedWriter | typing.BinaryIO = sys.stdout.buffer

    if out:
        f = open(out, "wb")

    f.write(decrypt_data(*[open(f, "rb").read() for f in inputs]))


cli.add_command(decrypt)
