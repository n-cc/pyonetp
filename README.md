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

- Encryption math is not bitwise, instead encryption is performed by adding and subtracting `bytes` objects, meaning this one time pad implementation is likely incompatible with others.
- Non-primary input files (ie keys) are only read until enough bytes are obtained to encrypt the primary input file (ie the data), with all other data being unused.
- All input files are loaded into memory at once, which may not be suitable for larger files.
