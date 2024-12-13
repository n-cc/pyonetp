"""Tests for operation functions."""

# noqa: D103

from pyonetp.exceptions import EmptyKeyError
from pyonetp.exceptions import KeyLengthError
from pyonetp.operations import decrypt
from pyonetp.operations import encrypt


def test_encrypt_single_ascii():
    assert encrypt(b"1234", b"5678") == b"fhjl"


def test_encrypt_mult_ascii():
    assert encrypt(b"1234", b"5678", b"9012") == b"\x9f\x98\x9b\x9e"


def test_encrypt_binary():
    assert encrypt(b"\x9c\x81\x4f\x90", b"\x47\x9d\x89\x11") == b"\xe3\x1e\xd8\xa1"


def test_decrypt_single_ascii():
    assert decrypt(b"fhjl", b"5678") == b"1234"


def test_decrypt_mult_ascii():
    assert decrypt(b"\x9f\x98\x9b\x9e", b"5678", b"9012") == b"1234"


def test_decrypt_binary():
    assert decrypt(b"\xe3\x1e\xd8\xa1", b"\x47\x9d\x89\x11") == b"\x9c\x81\x4f\x90"


def test_encrypt_truncated():
    try:
        encrypt(b"1234", b"5")  # == b"f"
    except KeyLengthError:
        assert True
    else:
        raise AssertionError


def test_encrypt_truncated_override():
    assert encrypt(b"1234", b"5", allow_input_wrapping=True) == b"fghi"


def test_decrypt_truncated():
    try:
        decrypt(b"fhjl", b"5")  # == b"1"
    except KeyLengthError:
        assert True
    else:
        raise AssertionError


def test_decrypt_truncated_override():
    assert decrypt(b"fghi", b"5", allow_input_wrapping=True) == b"1234"


def test_encrypt_empty():
    try:
        encrypt(b"1234", b"")
    except EmptyKeyError:
        assert True
    else:
        raise AssertionError


def test_decrypt_empty():
    try:
        decrypt(b"fhjl", b"")
    except EmptyKeyError:
        assert True
    else:
        raise AssertionError
