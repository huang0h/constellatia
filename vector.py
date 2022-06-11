import pygame
import math
import numpy as np
import scipy
from scipy import signal

# vectorscope based off of Wave Candy's vectorscope
class Vectorscope:
    def __init__(self, screen, width, height, x, y, max_amp):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.max_amp = max_amp

    def draw(self, left_samples, right_samples, resolution):
        # x is determined by proportion of magnitude on left/right
        # i.e. 100% of signal left = max on left axis
        # y is determined by ??? - needs more experimentation

        # split the left, right samples into indivudal windows, based on resolution, and get their averages
        left_windows = np.split(np.array(left_samples), np.arange(resolution, len(left_samples), resolution))[:-1]
        right_windows = np.split(np.array(right_samples), np.arange(resolution, len(right_samples), resolution))[:-1]
        
        left_windows = list(map(lambda l: np.sum(l) / len(l), left_windows))
        right_windows = list(map(lambda l: np.sum(l) / len(l), right_windows))

        points = []
        for left_avg, right_avg in zip(left_windows, right_windows):
            l_x = self.x - (self.width / 2) * (left_avg / self.max_amp)
            l_y = self.y - (self.height / 2) * (left_avg / self.max_amp)

            r_x = self.x + (self.width / 2) * (right_avg / self.max_amp)
            r_y = self.y - (self.height / 2) * (right_avg / self.max_amp)

            l_prop = abs(left_avg / (abs(left_avg) + abs(right_avg)))
            r_prop = abs(right_avg / (abs(left_avg) + abs(right_avg)))
            points.append( ( l_x * l_prop + r_x * r_prop, l_y * l_prop + r_y * r_prop ) )

        color = pygame.Color(255, 0, 0) #self.samples_to_hsla(list(map(lambda l, r: l + r / 2, left_samples, right_samples)))

        for point in points:
            pygame.draw.circle(self.screen, color, point, 5, 1)
        

    def samples_to_hsla(self, samples: list) -> pygame.Color:
        color: pygame.Color = pygame.Color(0, 0, 0)
        window = signal.windows.blackmanharris(10000)

        resample = signal.resample(samples, 10000)
        chunk_fft = np.abs(scipy.fft.fft(np.multiply(resample, window)))
        freq = np.argmax(chunk_fft[1:]) + 1

        if freq > 10000 or freq < 24:
            return color

        # formula adapted from https://en.wikipedia.org/wiki/Piano_key_frequencies
        hue = math.ceil(41.9 * math.log(freq / 440, 2) + 171.11)
        color.hsla = (hue, 100, 100, 100)
        return color
