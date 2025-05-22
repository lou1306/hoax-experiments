from pycontract.pycontract_core import (Event, HotState, Monitor, data, error,
                                        ok)


@data
class Acquire:
    thread: str
    lock: int


@data
class Release:
    thread: str
    lock: int


@data
class Free:
    memory: int


class M1(Monitor):
    """
    Basic property/
    """
    def transition(self, event):
        match event:
            case Acquire(thread, lock):
                return M1.DoRelease(thread, lock)

    @data
    class DoRelease(HotState):
        thread: str
        lock: int

        def transition(self, event):
            match event:
                case Acquire(thread, self.lock) if thread != self.thread:
                    return error('double acquisition')
                case Release(self.thread, self.lock):
                    return ok


def convert_line(ln: str) -> Event:
    if ln[0] == "a":
        return Acquire(thread=ln[2], lock=int(ln[1]))
    return Release(thread=ln[2], lock=int(ln[1]))
