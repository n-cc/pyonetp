"""Operations."""

import math
import typing

from pyonetp.exceptions import EmptyKeyError
from pyonetp.exceptions import KeyLengthError


def _parse_keys(f: typing.Callable[..., bytes]) -> typing.Callable[..., bytes]:
    def wrapper(*args: bytes, allow_input_wrapping: bool = False) -> bytes:
        keys = [args[0]]
        pk_len = len(keys[0])

        for idx, a in enumerate(args[1:]):
            a_len = len(a)

            if a_len == 0:
                raise EmptyKeyError(idx + 1)

            if a_len < pk_len:
                if allow_input_wrapping:
                    a = a * (math.floor(pk_len / a_len) + pk_len % a_len)
                else:
                    raise KeyLengthError(idx + 1)

            keys.append(a)

        return f(*keys)

    return wrapper


@_parse_keys
def encrypt(*args: bytes) -> bytes:
    """Encrypts byte objects."""

    def add(*args: int) -> int:
        return sum(args) % 256

    return bytes(list(map(add, *args)))


@_parse_keys
def decrypt(*args: bytes) -> bytes:
    """Decrypts byte objects."""

    def sub(*args: int) -> int:
        return (args[0] - sum(args[1:])) % 256

    return bytes(list(map(sub, *args)))
