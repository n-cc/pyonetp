import os

def generate_key(l):
    return os.urandom(l)

def encrypt(*args):
    def add(*args):
        return sum(args) % 256
    return bytes(list(map(add, *args)))

def decrypt(*args):
    def sub(*args):
        return (args[0] - sum(args[1:])) % 256
    return bytes(list(map(sub, *args)))
