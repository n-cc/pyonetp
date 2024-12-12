"""Operations."""


def encrypt(*args: bytes) -> bytes:
    """Encrypts byte objects."""

    def add(*args: int) -> int:
        return sum(args) % 256

    return bytes(list(map(add, *args)))


def decrypt(*args: bytes) -> bytes:
    """Decrypts byte objects."""

    def sub(*args: int) -> int:
        return (args[0] - sum(args[1:])) % 256

    return bytes(list(map(sub, *args)))
