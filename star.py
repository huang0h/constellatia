import pygame
from pygame.sprite import Sprite
import random

MAX_SIZE = 50

class Star(Sprite):

    def __init__(self, screen, amp_ratio, x, y):
        super().__init__()

        self.screen = screen
        self.size = amp_ratio * MAX_SIZE
        self.alpha = round(amp_ratio ** 0.5)
        self.x = x
        self.y = y
        
        self.dx = random.randint(-1, 1)
        self.dy = random.randint(-1, 1) if self.dx == 0 else 0

    def update(self, elapsed, dec = 0.1):
        self.size = max(0, self.size - dec * elapsed / 5)
        self.x += elapsed / 20 * self.dx
        self.y += elapsed / 20 * self.dy
        if self.size <= 0:
            self.kill()
    
    def draw(self, color: pygame.Color = pygame.Color(255, 255, 255)):
        pygame.draw.polygon(self.screen, 
        pygame.Color(self.alpha * color.r, self.alpha * color.g, self.alpha * color.b), 
        [(self.x + self.size / 2, self.y), 
        (self.x, self.y - self.size / 2),
        (self.x - self.size / 2, self.y), 
        (self.x, self.y + self.size / 2), 
        ])
    