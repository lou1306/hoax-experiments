from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from sys import stderr

from hoax.hoa import parse
from hoax.config.config import Configuration
from hoax.drivers import EndOfFiniteTrace

from pycontract_monitor import M1, convert_line

RUNS = 50
N = (2, 4, 8)
SIZES = (50, 100, 200)

print("[INFO] Setting up all automata. This might take a while")
all_automata = {}

with ThreadPoolExecutor() as exc:
    futures = {n: list() for n in N}
    for n in N:
        name = f"{n}locks{n}threads"
        files = list(str(x) for x in Path(name).glob("*.hoa"))
        all_automata[n] = list(exc.map(parse, files))
print("[INFO] Done.")


def bench_pycontracts(n, trace_size):
    name = f"{n}locks{n}threads"
    monitor = M1()
    with open(Path(name) / f"{name}.{trace_size}k.txt") as trace_file:
        t = datetime.now()
        for ln in trace_file:
            monitor.eval(convert_line(ln))
        monitor.end()
        dt = (datetime.now() - t).total_seconds()
        print(f"pycontracts,{n},{trace_size},{dt}", file=stderr)


def bench_hoax(n, trace_size):
    name = f"{n}locks{n}threads"
    automata = all_automata[n]
    config_file = Path(name) / f"{trace_size}k.toml"
    conf = Configuration.factory(config_file, automata, True)
    run = conf.get_runner()
    run.init()
    t = datetime.now()
    try:
        while True:
            run.step()
    except EndOfFiniteTrace as e:
        print(f"Stopping due to {repr(e)}")
    dt = (datetime.now() - t).total_seconds()
    print(f"hoax,{n},{trace_size},{dt}", file=stderr)


def main():
    print("tool,n,trace_size,time_seconds", file=stderr)
    for _ in range(RUNS):
        for n in N:
            for size in SIZES:
                bench_pycontracts(n, size)
                bench_hoax(n, size)


if __name__ == "__main__":
    main()
