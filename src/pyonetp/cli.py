import os
import sys
import click

from pyonetp.operations import encrypt as encrypt_data, decrypt as decrypt_data

@click.group()
def cli() -> None:
    "Encrypt and decrypt one time pads."
    pass

@click.command()
@click.argument('inputs', nargs=-1, required=True)
@click.option('--out', help="Write encrypted data to specified file (default: stdout)")
@click.option('--genkey', help="Generate a key to use for encryption and write it to the specified path", multiple=True)
def encrypt(inputs: tuple[str], out: str, genkey: tuple[str]) -> None:
    """
    Encrypt files.
    
    Accepts an arbitrary number of files as input. The first file is generally the data to be encrypted, and the remaining files are the encryption keys, though this is not required. The non-primary files must be at least as long as the primary file.
    """
    l = open(inputs[0]).seek(0, os.SEEK_END)

    for idx, i in enumerate(inputs[1:]):
        if open(i).seek(0, os.SEEK_END) < l:
            click.echo(f'Non-primary input "{i}" is shorter than primary input "{inputs[0]}", refusing to continue.')
            sys.exit(1)

    for kf in genkey:
        with open(kf, 'wb') as f:
            f.write(os.urandom(l))

    if out:
        f = (open(out, 'wb') if out else sys.stdout)
    else:
        f = sys.stdout.buffer

    f.write(encrypt_data(*[open(f, "rb").read() for f in inputs + genkey]))

cli.add_command(encrypt)

@click.command()
@click.argument('inputs', nargs=-1, required=True)
@click.option('--out', help="Write decrypted data to specified file (default: stdout)")
def decrypt(inputs: tuple[str], out: str) -> None:
    """
    Decrypt files.

    Accepts an arbitrary number of files as input. The first file is generally the file to be decrypted, and the remaining files are the encryption keys, though this is not required. The non-primary files must should be at least as long as the primary file.
    """
    l = open(inputs[0]).seek(0, os.SEEK_END)

    for idx, i in enumerate(inputs[1:]):
        if open(i).seek(0, os.SEEK_END) < l:
            click.echo(f'Non-primary input "{i}" is shorter than primary input "{inputs[0]}", refusing to continue.')
            sys.exit(1)

    if out:
        f = (open(out, 'wb') if out else sys.stdout)
    else:
        f = sys.stdout.buffer

    f.write(decrypt_data(*[open(f, "rb").read() for f in inputs]))

cli.add_command(decrypt)