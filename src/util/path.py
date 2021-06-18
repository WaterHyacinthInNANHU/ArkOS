import os

def touch(path: str):
    with open(path, 'a'):
        os.utime(path, None)


