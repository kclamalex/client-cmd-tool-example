import sys


def clear_stdout(string: str):
    """
    clear the stdout according to how many lines the string got
    """
    number_of_line = string.count("\n") + 1
    for _ in range(number_of_line):
        sys.stdout.write(f"\x1b[1A\r")
        sys.stdout.write("\x1b[2K\r")
