"""
В рк будут повороты, скалирование, изменение размера обьектов по формулам
"""

import pygame as pg
import pygame.display

pg.init()

screen: pg.Surface = pg.display.set_mode((600, 300))
some = pygame.image.load('some.png')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

class Sprite():
    def __init__(self, surface, image, x, y):
        self.surface: pg.Surface = surface
        self.image = image
        self.x, self.y = x, y
        self.angle = 0
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

    def update(self) -> None:
        self.rotate()
        self.surface.blit(self.rotated_image, (self.x, self.y))

    def rotate(self):
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.angle = self.angle + 15

running = True

cube = Sprite(screen, some, 100, 100)

clock = pygame.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(RED)

    cube.update()

    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)


pg.quit()