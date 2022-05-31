import matplotlib.pyplot
from random import shuffle


class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.view = f'({round(self.x, 1)}; {round(self.y, 1)})'

    def __repr__(self):
        return self.view


class Line:

    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.x = x1
        self.y = y1
        self.x2 = x2
        self.y2 = y2
        self.vertical = False
        self.horizontal = False
        self.slope = 0
        try:
            self.slope = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            self.slope = 1e100
            self.vertical = True
        if self.slope > 1e100:
            self.vertical = True
            self.slope = 1e100
        if self.slope < 1e-5:
            self.horizontal = True

        if self.horizontal:
            self.view = f'y = {round(self.y, 1)}'
        elif self.vertical:
            self.view = f'x = {round(self.x, 1)}'
        else:

            self.bias = ((y1 - self.slope * x1) + (y2 - self.slope * x2)) / 2
            bias_sign = '+' if self.bias > 0 else '-'
            self.view = f'y = {round(self.slope, 1)} * x {bias_sign} {round(abs(self.bias), 1)}'

    def __repr__(self):
        return self.view


class Triangle:

    def __init__(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.view = f'A({round(self.x1, 1)}; {round(self.y1, 1)}); B({round(self.x2, 1)}; {round(self.y2, 1)}); C({round(self.x3, 1)}; {round(self.y3, 1)})'

    def __repr__(self):
        return self.view


class Circle:

    def __init__(self, x_o: float, y_o: float, x_r: float, y_r: float):
        self.x_o = x_o
        self.y_o = y_o
        self.r = ((x_o - x_r) ** 2 + (y_o - y_r) ** 2) ** 0.5

        x_sign = '-' if self.x_o > 0 else '+'
        y_sign = '-' if self.y_o > 0 else '+'
        self.view = f'(x {x_sign} {round(abs(self.x_o), 1)})^2 + (y {y_sign} {round(abs(self.y_o), 1)})^2 = ({round(self.r, 1)})^2'

    def __repr__(self):
        return self.view


class GraphicsManager:

    def __init__(self, xlim=(-100, 100), ylim=(-50, 50)):
        self.objects = {
            Point: [],
            Line: [],
            Triangle: [],
            Circle: []
        }

        self.solve_line = None
        self.xlim = xlim
        self.ylim = ylim
        self.temp_points = []

    def set_limits(self, xlim, ylim):
        self.xlim = xlim
        self.ylim = ylim

    def __collect_points(self) -> tuple:
        x = []
        y = []
        for point in self.objects[Point]:
            x.append(point.x)
            y.append(point.y)
        return x, y

    def __collect_temp_points(self) -> tuple:
        x = []
        y = []
        for point in self.temp_points:
            x.append(point.x)
            y.append(point.y)
        return x, y

    def __collect_triangles(self) -> tuple:
        ab = []
        bc = []
        ac = []
        for triangle in self.objects[Triangle]:
            ab.append(([triangle.x1, triangle.x2], [triangle.y1, triangle.y2]))
            bc.append(([triangle.x2, triangle.x3], [triangle.y2, triangle.y3]))
            ac.append(([triangle.x1, triangle.x3], [triangle.y1, triangle.y3]))
        assert len(ab) == len(bc) == len(ac)
        return ab, bc, ac

    def points_in_circle(self, o_x, o_y, r):
        r_squared = r**2
        count = 0
        points = []
        for p in self.objects[Point]:
            if (p.x - o_x)**2 + (p.y - o_y)**2 <= r_squared:
                points.append(p)
                count += 1
        return points, count

    def solve(self):
        lines = self.objects[Line].copy()
        triangles = self.objects[Triangle].copy()
        max_line = None
        max_count = 0

        for line in lines:
            count = 0
            for triangle in triangles:
                if GraphicsManager.intersect(triangle, line):
                    count += 1
            if count > max_count:
                max_line = line
                max_count = count

        self.solve_line = max_line

    @staticmethod
    def intersect(tri: Triangle, line: Line) -> bool:
        def sign(n):
            if n > 0:
                return 1
            elif n == 0:
                return 0
            else:
                return -1

        def point_pos(x1, y1, x2, y2, x3, y3):
            return sign((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1))

        posA = point_pos(line.x, line.y, line.x2, line.y2, tri.x1, tri.y1)
        posB = point_pos(line.x, line.y, line.x2, line.y2, tri.x2, tri.y2)
        posC = point_pos(line.x, line.y, line.x2, line.y2, tri.x3, tri.y3)

        if posA == 0 or posB == 0 or posC == 0:
            return True

        if posA + posB == 0 or posA + posC == 0 or posB + posC == 0:
            return True

        return False

    def draw(self, ax):
        # Добавляем оси
        ax.axhline(y=0, color='black', linestyle='--')
        ax.axvline(color='black', linestyle='--')

        # Размещаем точки
        points_x, points_y = self.__collect_points()
        ax.scatter(points_x, points_y, color='orange', s=15, marker='o')

        # Размещаем прямые
        for line in self.objects[Line]:
            ax.axline((line.x, line.y), slope=line.slope, color='blue')

        # Размещаем треугольники
        ab, bc, ac = self.__collect_triangles()
        for i in range(len(ab)):
            ab_x, ab_y = ab[i]
            bc_x, bc_y = bc[i]
            ac_x, ac_y = ac[i]
            ax.plot(ab_x, ab_y, color='r')
            ax.plot(bc_x, bc_y, color='r')
            ax.plot(ac_x, ac_y, color='r')

        # Размещаем окружности
        for circle in self.objects[Circle]:
            ax.add_patch(matplotlib.pyplot.Circle((circle.x_o, circle.y_o),
                                                  circle.r, color='g', fill=False))

        # Размещаем временные точки
        temp_points_x, temp_points_y = self.__collect_temp_points()
        ax.scatter(temp_points_x, temp_points_y, color='brown', s=10, marker='o')

        if self.solve_line is not None:
            ax.axline((self.solve_line.x, self.solve_line.y), slope=self.solve_line.slope, color='green')

        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)
