import pygame

class Oscilloscope:
    
    def __init__(self, screen, width, height, x, y, max_amp):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.max_amp = max_amp

    def draw(self, window: list):
        for i, amp in enumerate(window):
            half_win = len(window) / 2
            x = ((i - half_win) / half_win) * self.width + self.x
            y = (amp / self.max_amp * self.height) + self.y
            pygame.draw.circle(self.screen, pygame.Color(255, 255, 255), (x, y), 1)