import math
from sys import argv, stderr, exit


try:
    if len(argv) < 3:
        raise ValueError
    width = int(math.log(int(argv[2]), 2))
except ValueError:
    print("usage: convert_trace.py [file] [num. locks/threads]", file=stderr)
    exit(1)


def json_bool(x, y):
    return 'true' if x == y else 'false'


def to_json():
    """Translation to json"""
    with open(argv[1]) as f:
        for line in f:
            a = json_bool(line[0], "a")
            print(f"""{{ "end": false, "a": {a}""", end="")
            tid = f"{bin(int(line[1])-1)[2:]:0>{width}}"
            lock = f"{bin(int(line[2])-1)[2:]:0>{width}}"
            for prefix, bits in (("t", tid), ("l", lock)):
                for i, x in enumerate(bits):
                    print(f""", "{prefix}{i}": {json_bool(x, '1')}""", end="")
            print(" }")

        aps = ("a", *(f"{x}{y}" for x in "tl" for y in "012"))
        aps_values = ", ".join(f""""{x}": false""" for x in aps)
        print(f"""{{ "end": true, {aps_values} }}""")


def to_simple():
    """Translation to hoa-exec simple txt format"""
    with open(argv[1]) as f:
        for line in f:
            if line[0] == "a":
                print("a")
            tid = f"{bin(int(line[1]))[2:]:0>{width}}"
            lock = f"{bin(int(line[2]))[2:]:0>{width}}"
            for prefix, bits in (("t", tid), ("l", lock)):
                for i, x in enumerate(bits):
                    if x == "1":
                        print(f"{prefix}{i}")
            print()
        print("end")
        print()


to_simple()
