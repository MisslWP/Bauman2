from dataclasses import dataclass
from typing import Union
from math import *
import numpy as np

@dataclass
class RootData:
    a: float
    b: float
    x: float
    f_x: float
    iters: float
    err_code: int

class Function:
    def __init__(self, s, eps, err_callback=None):
        def f(x: float):
            return eval(s)

        self.func = f
        self.eps = eps
        self.err = err_callback

    def __call__(self, x):
        res = 0
        try:
            res = self.func(x)
        except (NameError, ZeroDivisionError, RuntimeWarning) as e:
            self.err(e)
        return res

    def derivative(self, x):
        return (self.func(x + self.eps) - self.func(x)) / self.eps


class Finder:
    def __init__(self, func: Function, eps, segments):
        self.func = func
        self.eps = eps
        self.segments = segments

    def find_all(self):
        min_x = []
        max_x = []
        for seg in self.segments:
            ix, ax = self._grad_descent(seg[0], seg[1])
            if ix is not None:
                min_x.append(ix)
            if ax is not None:
                max_x.append(ax)
        return min_x, max_x

    def _grad_descent(self, low, high):
        f = self.func
        df = self.func.derivative
        iters_count = 5000
        lr_base = 0.05

        def find_loc_extremum(iters=iters_count, lr=lr_base, minimum=True):
            x0 = np.random.uniform(low, high)
            x = x0
            eps = 1e-10
            delta = 1
            _iter = 1
            found = True
            while delta > eps:
                if _iter > iters:
                    found = False
                    break
                _iter += 1
                f_before = f(x)
                if minimum:
                    x -= df(x) / _iter ** 0.5 * lr
                else:
                    x += df(x) / _iter ** 0.5 * lr
                delta = abs(f_before - f(x))

            return x if found else None

        mn = find_loc_extremum()
        mx = find_loc_extremum(minimum=False)
        return mn, mx


class SteffenserRule:
    def __init__(self, segments, eps, n_max, func):
        self.segments = segments
        self.eps = eps
        self.n_max = n_max
        self.func = func

    def next(self, x: float):
        return x - (self.func(x) * self.func(x) / (self.func(x + self.func(x)) - self.func(x)))

    def _is_valid_segment(self, segment: tuple):
        fa = self.func(segment[0])
        fb = self.func(segment[1])
        return fa * fb < 0

    def _prepare_segments(self):
        self.segments = filter(self._is_valid_segment, self.segments)

    def is_precise(self, prev_x, cur_x):
        return abs(self.func(prev_x) - self.func(cur_x)) < self.eps

    def find_root_on_segment(self, segment: tuple) -> Union[RootData, None]:
        i = 0
        prev_x = (segment[0] + segment[1]) / 2
        cur_x = prev_x
        too_many_iters = True
        while i < self.n_max:
            i += 1
            try:
                cur_x = self.next(cur_x)
            except ZeroDivisionError:
                prev_x = cur_x
                too_many_iters = False
                break
            if self.is_precise(prev_x, cur_x):
                too_many_iters = False
                break
            prev_x = cur_x
        err_code = 0
        if not (segment[0] <= prev_x < segment[1]):
            err_code = 2
        if self.func(prev_x) > self.eps:
            err_code = 2
        if too_many_iters:
            err_code = 1

        return RootData(segment[0], segment[1], prev_x, self.func(prev_x), i, err_code)

    def get_root_data(self):
        self._prepare_segments()
        return list(filter(lambda x: x is not None, map(self.find_root_on_segment, self.segments)))


class RootFinder:

    def __init__(self, a: float, b: float, h: float, n_max: int, eps: float, func: str):
        self.f_str: str = func
        self.n_max = n_max
        self.eps = eps
        self.f = Function(func, eps / 10)
        self.results = []
        self.a = a
        self.b = b
        self.h = h
        values = np.concatenate((np.arange(a, b, h), [b]))
        segments = []
        for i in range(len(values) - 1):
            segments.append((float(values[i]), float(values[i + 1])))
        rule = SteffenserRule(segments, self.eps, self.n_max, self.f)
        self.roots = rule.get_root_data()
        self.calc_x = np.concatenate((np.arange(a, b, h / 10), [b]))
        self.calc_y = np.array(list(map(self.f, self.calc_x)))
        finder = Finder(self.f, self.eps, segments)
        all = finder.find_all()
        self.extremum = all[0] + all[1]

    def plot(self, canvas):
        plt = canvas.axes
        x = self.calc_x
        y = self.calc_y
        root_x = []
        root_y = []
        extr_x = []
        extr_y = []
        for r in self.roots:
            if r.err_code != 0:
                continue
            root_x.append(r.x)
            root_y.append(r.f_x)
        for ext in self.extremum:
            if ext < self.a or ext > self.b:
                continue
            extr_x.append(ext)
            extr_y.append(self.f(ext))
        smooth = np.gradient(np.gradient(y))
        inflect = np.where(np.diff(np.sign(smooth)))[0]
        plt.plot(x, y)
        plt.axhline(y=0, color='black', linewidth=1)
        plt.legend([self.f_str, 'y=0'])
        plt.scatter(root_x, root_y, color='orange', s=50, marker='o')
        plt.scatter(extr_x, extr_y, color='blue', s=30, marker='o')
        plt.scatter(x[inflect], y[inflect], color='red', s=40, marker='o')

