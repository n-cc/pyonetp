# pyonetp

Demo implementation of a data-agnostic one time pad in Python, supporting an arbitrary number of input files (keys or data).

## Example

```
$ echo "Hello world 😀!" > original
$ dd if=/dev/urandom of=key1 bs=1 count=20 status=none
$ dd if=/dev/urandom of=key2 bs=1 count=20 status=none
$ pyonetp encrypt original key1 key2 --out encrypted
$ xxd encrypted
00000000: 8e45 ad9b 5a14 cad7 8400 bd9c f7d7 27ed  .E..Z.........'.
00000010: d4fc                                     ..
$ pyonetp decrypt encrypted key1 key2
Hello world 😀!
$
```

## Known Limitations

- Encryption math is not (currently) bitwise, instead encryption is performed by adding and subtracting `bytes` objects.
- The cli enforces that non-primary input files (ie keys) are equal or greater in length than the primary input file (ie the data), but this is not enforced or sanity checked on the backend, which will lead to truncated data if non-primary input files are shorter than the primary input file.
- Non-primary input files (ie keys) are only read until enough bytes are obtained to encrypt the primary input file (ie the data), with all other data being unused.
- Keys generated with `--genkey` are as secure as `os.urandom` is on your machine.
- All input files are loaded into memory at once, which may not be suitable for larger files.
