"""Utility classes and functions."""


class KeyLengthError(Exception):
    """Indicates a provided non-primary input is shorter than the primary input."""

    def __init__(self, idx: int) -> None:
        """Init."""
        super().__init__()

        self.idx = idx


class EmptyKeyError(Exception):
    """Indicates a provided non-primary key is empty."""

    def __init__(self, idx: int) -> None:
        """Init."""
        super().__init__()

        self.idx = idx
