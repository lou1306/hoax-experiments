from random import choice
from sys import argv, stderr, exit

if len(argv) < 3:
    print("Usage: gen_trace.py {length} {num locks/threads}", file=stderr)
    exit(1)
try:
    n = int(argv[1])
    lt = int(argv[2])
    if n < 2 or lt < 2 or lt > 9:
        raise ValueError
except ValueError:
    print(f"Invalid args '{argv[1:]}'")
for _ in range(n):
    print(choice("ar"), choice(range(lt)), choice(range(lt)), sep="")
