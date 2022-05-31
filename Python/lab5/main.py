# Сделать анимацию в pygame минимум 2 движущихся объекта по разному
import math
import time
from typing import List, Dict, Tuple, Optional, Callable, Any

import pygame
import physics
from physics import Force, PhysicsComponent, ForceSequence
from property import Property

SIZE = WIDTH, HEIGHT = 800, 600
bg = pygame.image.load('resources/bg.png')
bg_hunt = pygame.image.load('resources/bg_hunt.png')
car = pygame.image.load('resources/car_clean.png')
car_broken = pygame.image.load('resources/car_broken.png')
stone = pygame.image.load('resources/stone.png')
cabbage = pygame.image.load('resources/cabbage.png')
boom = pygame.image.load('resources/boom.png')
h1 = pygame.image.load('resources/human1.png')
h2 = pygame.image.load('resources/human2.png')
h3 = pygame.image.load('resources/human3.png')
hc1 = pygame.image.load('resources/human1_cabbage.png')
hc2 = pygame.image.load('resources/human2_cabbage.png')
hc3 = pygame.image.load('resources/human3_cabbage.png')
war = pygame.image.load('resources/war.png')
end = pygame.image.load('resources/end.png')
FPS = 60
physics.TPS = FPS


class MovingObject:
    def __init__(self, x: float, y: float, img: pygame.image):
        self.physics = PhysicsComponent(x, y)
        self.img = img

    def update(self, display: pygame.Surface):
        self.physics.update_forces()
        display.blit(self.img, (round(self.physics.x), round(self.physics.y)))

    def init(self, x: float, y: float):
        self.physics = PhysicsComponent(x, y)


class Stage:
    def __init__(self, background: pygame.image, display: pygame.Surface,
                 on_ended: Optional[Callable[..., Any]] = None):
        self.bg: pygame.image = background
        self.display: pygame.Surface = display
        self.objects: Dict[str, Tuple[MovingObject, bool]] = {}
        self.end_callback = on_ended

    def add_object(self, tag: str, obj: MovingObject) -> None:
        self.objects[tag] = (obj, True)

    def toggle_object(self, tag: str):
        self.objects[tag] = self.objects[tag][0], not self.objects[tag][1]

    def update(self):
        self.display.blit(self.bg, (0, 0))
        for tag in self.objects:
            obj, is_active = self.objects[tag]
            if is_active:
                obj.update(self.display)

    def end(self):
        if self.end_callback is not None:
            self.end_callback()


class StageController:
    def __init__(self, display: pygame.Surface):
        self.display = display
        self.stages: List[Tuple[Stage, float]] = []
        self.cur_stage: Optional[Tuple[Stage, float, float]] = None
        self.running = False
        self.clock = pygame.time.Clock()

    def add_stage(self, background: pygame.image, ttl: float) -> Stage:
        stage = Stage(background, self.display)
        self.stages.append((stage, ttl))
        return stage

    def stop(self):
        self.running = False

    def ended(self):
        return self.cur_stage is None and len(self.stages) == 0

    def update(self):
        if self.ended():
            self.stop()
            return

        if self.cur_stage is None:
            stage, ttl = self.stages.pop(0)
            self.cur_stage = (stage, ttl, time.time())

        stage, ttl, started_time = self.cur_stage

        stage.update()

        if 0 < ttl <= time.time() - started_time:
            stage.end()
            self.cur_stage = None

    def run(self):
        self.running = True
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()

            pygame.display.update()
            self.clock.tick(FPS)


def main():
    pygame.init()

    screen = pygame.display.set_mode(SIZE)

    controller = StageController(screen)

    car_object = MovingObject(0, 340, car)
    car_broken_object = MovingObject(0, 0, car_broken)
    stone_object = MovingObject(380, 350, stone)
    cab1_object = MovingObject(0, 0, cabbage)
    cab2_object = MovingObject(0, 0, cabbage)
    cab3_object = MovingObject(0, 0, cabbage)
    h1_object = MovingObject(830, 360, h1)
    h2_object = MovingObject(500, 500, h2)
    h3_object = MovingObject(-40, 370, h3)
    war_object = MovingObject(190, 280, war)
    hc1_object = MovingObject(0, 0, hc1)
    hc2_object = MovingObject(0, 0, hc2)
    hc3_object = MovingObject(0, 0, hc3)

    def return_to_road():
        car_object.init(-160, 310)
        car_object.physics.apply_force(Force.move(800, 0, 1.5))

    def set_car_broken():
        phys = car_object.physics
        car_broken_object.init(phys.x, phys.y)
        cab1_object.init(phys.x + 40, phys.y + 90)
        cab2_object.init(phys.x + 70, phys.y + 100)
        cab3_object.init(phys.x + 100, phys.y + 85)

    def set_humans():
        h1_p = h1_object.physics
        h2_p = h2_object.physics
        h3_p = h3_object.physics
        c3 = cab3_object.physics
        c2 = cab2_object.physics
        c1 = cab1_object.physics
        walk_time = 6
        h1_p.apply_force(Force.from_to(h1_p.x, h1_p.y, c3.x, c3.y, walk_time))
        h2_p.apply_force(Force.from_to(h2_p.x, h2_p.y, c2.x, c2.y, walk_time))
        h3_p.apply_force(Force.from_to(h3_p.x, h3_p.y, c1.x, c1.y, walk_time))

    def set_cabbagge():
        h1_p = h1_object.physics
        h2_p = h2_object.physics
        h3_p = h3_object.physics
        hc1_object.init(h1_p.x, h1_p.y)
        hc2_object.init(h2_p.x, h2_p.y)
        hc3_object.init(h3_p.x, h3_p.y)
        hc1_p = hc1_object.physics
        hc2_p = hc2_object.physics
        hc3_p = hc3_object.physics
        hc1_p.apply_force(Force.from_to(hc1_p.x, hc1_p.y, 1000, 360, 4.2))
        hc2_p.apply_force(Force.from_to(hc2_p.x, hc2_p.y, -200, 440, 5))
        hc3_p.apply_force(Force.from_to(hc3_p.x, hc3_p.y, -100, 330, 4))

    stage1 = controller.add_stage(bg, 8)
    stage2 = controller.add_stage(bg, 0.8)
    stage3 = controller.add_stage(boom, 2)
    stage4 = controller.add_stage(bg, 3)
    stage5 = controller.add_stage(bg_hunt, 2)
    stage6 = controller.add_stage(bg, 6)
    stage7 = controller.add_stage(bg, 2)
    stage8 = controller.add_stage(bg, 4.5)
    stage9 = controller.add_stage(end, 10)

    stage1.add_object('car', car_object)
    stage2.add_object('stone', stone_object)
    stage2.add_object('car', car_object)
    stage1.end_callback = return_to_road
    stage2.end_callback = set_car_broken
    stage4.add_object('car', car_broken_object)
    stage4.add_object('cab1', cab1_object)
    stage4.add_object('cab2', cab2_object)
    stage4.add_object('cab3', cab3_object)
    stage5.add_object('car', car_broken_object)
    stage5.add_object('cab1', cab1_object)
    stage5.add_object('cab2', cab2_object)
    stage5.add_object('cab3', cab3_object)
    stage5.end_callback = set_humans
    stage6.add_object('car', car_broken_object)
    stage6.add_object('cab1', cab1_object)
    stage6.add_object('cab2', cab2_object)
    stage6.add_object('cab3', cab3_object)
    stage6.add_object('h1', h1_object)
    stage6.add_object('h3', h3_object)
    stage6.add_object('h2', h2_object)
    stage7.add_object('car', car_broken_object)
    stage7.add_object('cab1', cab1_object)
    stage7.add_object('cab2', cab2_object)
    stage7.add_object('cab3', cab3_object)
    stage7.add_object('h1', h1_object)
    stage7.add_object('h3', h3_object)
    stage7.add_object('h2', h2_object)
    stage7.add_object('war', war_object)
    stage7.end_callback = set_cabbagge
    stage8.add_object('car', car_broken_object)
    stage8.add_object('hc2', hc2_object)
    stage8.add_object('hc1', hc1_object)
    stage8.add_object('hc3', hc3_object)

    seq1 = ForceSequence().add(Force(Property(2), Property(-0.1), 2)) \
        .add(Force(Property(1.5), Property(0), 1)) \
        .add(Force(Property(1), Property(-0.5), 2)) \
        .add(Force(Property(4), Property(0), 2))

    def fy(x: float) -> float:
        return -math.sin(4 * x) / 2

    zigzag = Force(Property(0), Property.func(fy), 7)

    car_object.physics.apply_force(seq1)
    car_object.physics.apply_force(zigzag)

    controller.run()


if __name__ == '__main__':
    main()
    pygame.quit()
