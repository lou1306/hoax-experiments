from sys import argv, stderr, exit
import math

if len(argv) < 2:
    print("Usage: gen_ltl.py {num locks/threads}", file=stderr)
    exit(1)
try:
    n = int(argv[1])
    if n < 2:
        raise ValueError
    bits = int(math.log(n, 2))
except ValueError:
    print(f"Invalid args '{argv[1:]}'")


def to_aps(num, prefix, width):
    digits = f"{bin(num)[2:]:0>{width}}"
    return " & ".join(
        f" ({prefix}{i})" if x == "1" else f"!({prefix}{i})"
        for i, x in enumerate(digits))


def no_double_acquire(thread, lock):
    t_aps = to_aps(thread, "t", bits)
    l_aps = to_aps(lock, "l", bits)
    return f"G ((!(end) & a & {t_aps} & {l_aps}) -> ((!(a) & {t_aps} & {l_aps}) R !(a & !({t_aps}) & {l_aps})))"  # noqa: E501


def release_before_end(thread, lock):
    t_aps = to_aps(thread, "t", bits)
    l_aps = to_aps(lock, "l", bits)
    return f"G ((!(end) & a & {t_aps} & {l_aps}) -> (!(end) W (!(a) & {t_aps} & {l_aps})))"  # noqa: E501


for thread in range(n):
    for lock in range(n):
        print(no_double_acquire(thread, lock))

for thread in range(n):
    for lock in range(n):
        print(release_before_end(thread, lock))
