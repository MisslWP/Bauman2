from math import sin, cos
from typing import Callable, List, Optional, Union, Any
from property import Property

TPS = 60


def __identity(x: float) -> float:
    return x


identity = Property(__identity, False)


class Force:
    def __init__(self, dx: Property[float], dy: Property[float], seconds: float,
                 ft: Property[float] = identity):
        self.dx: Property[float] = dx
        self.dy: Property[float] = dy
        self.ft = ft
        self.ticks: int = round(abs(seconds) * TPS)
        self.time = 0

    def tick(self, callback: Callable[[float, float], None]):
        if self.ended():
            return
        t_param = self.ft.value(self.time)
        callback(self.dx.value(t_param), self.dy.value(t_param))
        self.ticks -= 1
        self.time += 1 / TPS

    def ended(self) -> bool:
        return self.ticks == 0

    @staticmethod
    def by_scalar(scalar: float, angle: float, seconds: float):
        dx = scalar * cos(angle)
        dy = scalar * sin(angle)
        return Force(Property(dx), Property(dy), seconds)

    @staticmethod
    def from_to(x1: float, y1: float, x2: float, y2: float, seconds: float):
        return Force.move(x2 - x1, y2 - y1, seconds)

    @staticmethod
    def move(x: float, y: float, seconds: float):
        ticks = round(seconds * TPS)
        dx = x / ticks
        dy = y / ticks
        return Force(Property(dx), Property(dy), seconds)

    @staticmethod
    def nothing(seconds: float):
        return Force(Property(0), Property(0), seconds)


class ForceSequence:
    def __init__(self):
        self.forces: List[Force] = []
        self.cur_force: Optional[Force] = None

    def ended(self) -> bool:
        return len(self.forces) == 0 and self.cur_force is None

    def tick(self, callback: Callable[[float, float], Any]):
        if self.ended():
            return

        if self.cur_force is None:
            if len(self.forces) > 0:
                self.cur_force = self.forces.pop(0)
                self.tick(callback)
        else:
            self.cur_force.tick(callback)
            if self.cur_force.ended():
                self.cur_force = None

    def add(self, force: Force):
        self.forces.append(force)
        return self


class PhysicsComponent:

    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.forces: List[Union[Force, ForceSequence]] = []

    def apply_force(self, force: Union[Force, ForceSequence]):
        self.forces.append(force)

    def update_forces(self):
        for force in self.forces:
            if force.ended():
                self.forces.remove(force)
            else:
                force.tick(self.move)

    def move(self, x: float, y: float):
        self.x += x
        self.y += y

    def set_pos(self, x: float, y: float):
        self.x = x
        self.y = y
