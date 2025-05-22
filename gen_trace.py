import random
from random import choice
from sys import argv, stderr, exit


def usage():
    print("Usage: gen_trace.py [length] [num locks/threads] [seed]", file=stderr)  # noqa: E501
    exit(1)


if len(argv) < 4:
    usage()
try:
    n = int(argv[1])
    lt = int(argv[2])
    seed = int(argv[3])
    if n < 2 or lt < 2 or lt > 9:
        raise ValueError
except ValueError:
    print(f"Invalid args '{argv[1:]}'")
    usage()

random.seed(seed)
for _ in range(n):
    print(choice("ar"), choice(range(lt)), choice(range(lt)), sep="")
