from typing import Tuple

import pygame as pg
from math import sin, cos, pi
import math

pg.init()

screen: pg.Surface = pg.display.set_mode((600, 400))
surf = pg.Surface((100, 100))

KOL_COL = (100, 100, 100)
HAIR_COL = (0, 200, 0)
MOUTH_COL = (250, 0, 50)
EYE_COL = (150, 150, 0)

orig_points = [(100, 100), (200, 100), (100, 200)]

def rotate_polygon(origin, points, angle) :
    angle = math.radians(angle)
    rotated_polygon = []
    x0, y0 = origin

    for point in points:
        x, y = point[0] - x0, point[1] - y0
        x, y = (x * math.cos(angle) - y * math.sin(angle),
                      x * math.sin(angle) + y * math.cos(angle))
        x, y = x + x0, y + y0
        rotated_polygon.append((x, y))

    return rotated_polygon

class Kolobok:
    def __init__(self, x, y):
        self.lines = []
        self.mouth = [(x, y+10), (x+20, y+20), (x-20, y + 20)]
        self.body = (x, y)
        self.radius = 30
        self.angular = 1
        self.linear = 1
        self.lines.append([(x, y - 10), (x - 10, y - 30)])
        self.lines.append([(x, y - 10), (x, y - 30)])
        self.lines.append([(x, y - 10), (x + 10, y - 30)])
        self.eyes = []
        self.eyes.append([(x+25, y - 5), (x + 20, y - 10), (x + 15, y - 5), (x + 20, y + 5)])
        self.eyes.append([(x - 25, y - 5), (x - 20, y - 10), (x - 15, y - 5), (x - 20, y + 5)])
        self.angle = 0

    def update_all(self):
        x, y = self.body
        self.lines.clear()
        self.mouth = [(x, y + 10), (x + 20, y + 20), (x - 20, y + 20)]
        self.lines.append([(x, y - 10), (x - 10, y - 30)])
        self.lines.append([(x, y - 10), (x, y - 30)])
        self.lines.append([(x, y - 10), (x + 10, y - 30)])
        self.eyes.clear()
        self.eyes.append([(x + 25, y - 5), (x + 20, y - 10), (x + 15, y - 5), (x + 20, y + 5)])
        self.eyes.append([(x - 25, y - 5), (x - 20, y - 10), (x - 15, y - 5), (x - 20, y + 5)])

    def draw(self, surf):
        self.update_all()
        pg.draw.circle(surf, KOL_COL, self.body, self.radius)
        pg.draw.polygon(surf, MOUTH_COL, rotate_polygon(self.body, self.mouth, self.angle))
        for line in self.lines:
            line = rotate_polygon(self.body, line, self.angle)
            pg.draw.polygon(surf, HAIR_COL, line, 1)
        for eye in self.eyes:
            eye = rotate_polygon(self.body, eye, self.angle)
            pg.draw.polygon(surf, EYE_COL, eye)

        self.body = self.body[0] + self.linear, self.body[1]
        self.angle += self.angular


center = sum(map(lambda x: x[0], orig_points))/3, sum(map(lambda x: x[1], orig_points))/3

clock = pg.time.Clock()

kolobok = Kolobok(50, 300)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((255, 255, 255))
    kolobok.draw(screen)

    clock.tick(100)
    pg.display.update()
    pg.display.flip()


pg.quit()