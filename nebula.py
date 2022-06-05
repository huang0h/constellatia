import pygame
from pygame.sprite import Sprite
from numpy import random
import math

MAX_STARS = 200
MAX_RADIUS = 500

class Nebula(Sprite):
    def __init__(self, screen: pygame.display, x: float, y: float, amp_ratio: float, color: pygame.Color):
        super().__init__()

        self.screen = screen
        self.x = x
        self.y = y
        self.color = color

        self.dx = random.default_rng().random() - 0.5
        self.dy = random.default_rng().random() - 0.5

        self.stars = [self.rand_star(self.x, self.y, amp_ratio) for i in range(math.ceil(amp_ratio * MAX_STARS))]
        self.counter = 0

    def rand_star(self, x: float, y: float, amp_ratio: float) -> tuple:
        d = (random.default_rng().normal(0, 0.2) + 0.3) * MAX_RADIUS * amp_ratio
        angle = random.default_rng().random() * 2 * math.pi
        return (x + d * math.cos(angle), y + d * math.sin(angle))

    def update(self, elapsed: float, dec: float = 0.1):
        self.counter += elapsed / 4 * dec
        if self.counter > 1:
            self.stars.pop(math.floor(random.default_rng().random() * len(self.stars)))
            self.counter = 0
        if len(self.stars) == 0:
            self.kill()
        else:
            self.stars = list(map(
            lambda t: (t[0] + self.dx * elapsed / 30, t[1] + self.dy * elapsed / 30), self.stars))

    def draw(self):
        for coord in self.stars:
            pygame.draw.circle(self.screen, self.color, coord, 2)

# class Nebula(Sprite):
#     def __init__(self, screen: pygame.display, x: float, y: float, amp_ratio: float, color: pygame.Color):
#         super().__init__()

#         self.screen = screen
#         self.x = x
#         self.y = y
#         self.color = color

#         self.stars = [self.rand_star(self.x, self.y) for i in range(math.ceil(amp_ratio * MAX_STARS))]
#         self.counter = 0

#     def rand_star(self, x: float, y: float) -> Star:
#         d = (random.default_rng().normal(0, 0.3) + 0.5) * MAX_RADIUS
#         angle = random.default_rng().random() * 2 * math.pi

#         return Star(self.screen, 0.3, 
#             x + d * math.cos(angle), 
#             y + d * math.sin(angle))

#     def update(self, elapsed: float, dec: float = 0.1):
#         for s in self.stars:
#             s.update(elapsed / 3, dec)

#         self.counter += elapsed / 10 * dec
#         if self.counter > 1:
#             self.stars.pop(math.floor(random.default_rng().random() * len(self.stars)))
#             self.counter = 0
#         if len(self.stars) == 0:
#             self.kill()

#     def draw(self):
#         for s in self.stars:
#             s.draw(self.color)