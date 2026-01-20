import sys


def check_arg() -> bool:

    if len(sys.argv) != 2:
        raise Arg
    return True
