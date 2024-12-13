"""Tests for cli functions."""

from click.testing import CliRunner

from pyonetp.cli import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert "Encrypt and decrypt one time pads." in result.output


def test_cli_encrypt_single_ascii_to_file(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "encrypt",
            "tests/samples/input1",
            "tests/samples/key1",
            "--out",
            f"{tmpdir}/test_cli_encrypt_single_ascii_to_file",
        ],
    )
    assert result.exit_code == 0
    assert result.output == ""

    with open(f"{tmpdir}/test_cli_encrypt_single_ascii_to_file", "rb") as out, open(
        "tests/samples/i1k1", "rb"
    ) as expected:
        assert out.read() == expected.read()


def test_cli_encrypt_mult_ascii_to_file(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "encrypt",
            "tests/samples/input1",
            "tests/samples/key1",
            "tests/samples/key2",
            "--out",
            f"{tmpdir}/test_cli_encrypt_mult_ascii_to_file",
        ],
    )
    assert result.exit_code == 0
    assert result.output == ""

    with open(f"{tmpdir}/test_cli_encrypt_mult_ascii_to_file", "rb") as out, open(
        "tests/samples/i1k1k2", "rb"
    ) as expected:
        assert out.read() == expected.read()


def test_cli_encrypt_binary_to_file(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "encrypt",
            "tests/samples/input2",
            "tests/samples/key1",
            "--out",
            f"{tmpdir}/test_cli_encrypt_binary_to_file",
        ],
    )
    assert result.exit_code == 0
    assert result.output == ""

    with open(f"{tmpdir}/test_cli_encrypt_binary_to_file", "rb") as out, open(
        "tests/samples/i2k1", "rb"
    ) as expected:
        assert out.read() == expected.read()


def test_cli_decrypt_single_ascii_to_file(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "decrypt",
            "tests/samples/i1k1",
            "tests/samples/key1",
            "--out",
            f"{tmpdir}/test_cli_decrypt_single_ascii_to_file",
        ],
    )
    assert result.exit_code == 0
    assert result.output == ""

    with open(f"{tmpdir}/test_cli_decrypt_single_ascii_to_file", "rb") as out, open(
        "tests/samples/input1", "rb"
    ) as expected:
        assert out.read() == expected.read()


def test_cli_decrypt_mult_ascii_to_file(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "decrypt",
            "tests/samples/i1k1k2",
            "tests/samples/key1",
            "tests/samples/key2",
            "--out",
            f"{tmpdir}/test_cli_decrypt_mult_ascii_to_file",
        ],
    )
    assert result.exit_code == 0
    assert result.output == ""

    with open(f"{tmpdir}/test_cli_decrypt_mult_ascii_to_file", "rb") as out, open(
        "tests/samples/input1", "rb"
    ) as expected:
        assert out.read() == expected.read()


def test_cli_decrypt_binary_to_file(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "decrypt",
            "tests/samples/i2k1",
            "tests/samples/key1",
            "--out",
            f"{tmpdir}/test_cli_decrypt_binary_to_file",
        ],
    )
    assert result.exit_code == 0
    assert result.output == ""

    with open(f"{tmpdir}/test_cli_decrypt_binary_to_file", "rb") as out, open(
        "tests/samples/input2", "rb"
    ) as expected:
        assert out.read() == expected.read()


def test_cli_encrypt_to_stdout(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["encrypt", "tests/samples/input1", "tests/samples/key1"]
    )
    assert result.exit_code == 0
    assert result.output != ""


def test_cli_encrypt_genkey(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "encrypt",
            "tests/samples/input1",
            "--genkey",
            f"{tmpdir}/test_cli_encrypt_genkey_key",
        ],
    )
    assert result.exit_code == 0
    assert result.output != ""

    with open(f"{tmpdir}/test_cli_encrypt_genkey_key", "rb") as key, open(
        "tests/samples/input1", "rb"
    ) as sample:
        assert len(key.read()) == len(sample.read())


def test_cli_encrypt_truncated(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "encrypt",
            "tests/samples/input1",
            "tests/samples/key3",
            "--out",
            f"{tmpdir}/test_cli_encrypt_truncated",
        ],
    )
    assert result.exit_code == 1
    assert (
        "Non-primary input tests/samples/key3 is shorter than primary input tests/samples/input1, refusing to continue."
        in result.output
    )


def test_cli_decrypt_truncated(tmpdir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "decrypt",
            "tests/samples/i1k1",
            "tests/samples/key3",
            "--out",
            f"{tmpdir}/test_cli_decrypt_truncated",
        ],
    )
    assert result.exit_code == 1
    assert (
        "Non-primary input tests/samples/key3 is shorter than primary input tests/samples/i1k1, refusing to continue."
        in result.output
    )
