# you might need to install these:
# pip install pydub
# pip install pygame
# pip install scipy
from pydub import AudioSegment
import pygame

import math
import numpy as np
import random

from star import Star
from nebula import Nebula
from oscilloscope import Oscilloscope
from vector import Vectorscope

# config vars - edit these to alter the visualizer
FILENAME = "testaudio/sinetest.mp3"

WINDOW_SIZE = 400
HOP_SIZE = 100

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
FPS = 60

MAX_NEB_CTDOWN = 200
MAX_STARS = 15

SCOPE_WIDTH = 600
SCOPE_HEIGHT = 375
GATE = 0 # out of 1
STAR_DECAY = 0.5 # out of 1

def rms(samples: list) -> float:
    return (np.dot(samples, samples) / len(samples)) ** 0.5

def gravitate(point: tuple, origin: tuple, g: float) -> tuple:
    delta_sqr = tuple(map(lambda o, p: ((o - p) ** 1) * np.sign(o - p), origin, point))
    return tuple(map(
        lambda d, p: p + g / d if not d == 0 else p, delta_sqr, point
    ))

def rand_color(base: int) -> pygame.Color:
    return pygame.Color(
        round(random.random() * (255 - base) + base), 
        round(random.random() * (255 - base) + base),
        round(random.random() * (255 - base) + base))

# process audio into 1-d array of average samples

audio = AudioSegment.from_file(FILENAME)

SAMPLE_RATE = audio.frame_rate
NUM_SAMPLES = math.floor(len(audio) / 1000 * SAMPLE_RATE)

monos: list = audio.split_to_mono()
channel_samples: list = [mono.get_array_of_samples() for mono in monos]

left_samples: list = []
right_samples: list = []
avg_sample: list = []
if len(channel_samples) == 1:
    avg_sample = channel_samples[0]
    left_samples = channel_samples[0]
    right_samples = channel_samples[0]
else:
    avg_sample = list(map(lambda x, y: (x + y) / 2,
                      channel_samples[0], channel_samples[1]))
    left_samples, right_samples = channel_samples

frame = 0
MAX_AMP = 2 ** (audio.sample_width * 8 - 1)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CONSTELLATIA v0.4")
pygame.mixer.music.load(FILENAME)

time_since_prev_update = 999999
total_elapsed = 0

smp_per_second = math.floor(SAMPLE_RATE / 1000)
pause = False

stars = pygame.sprite.Group()
nebulae = pygame.sprite.Group()
neb_ctdown = 0

# does nothing right now - looking to implement later
gravitation = 0
mouse_down = False
mouse = (0, 0)

clock = pygame.time.Clock()
pygame.mixer.music.play()
screens = []
RUNNING = True
RECORDING = False

oscope = Oscilloscope(screen, SCOPE_WIDTH, SCOPE_HEIGHT, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, MAX_AMP)
vscope = Vectorscope(screen, SCOPE_WIDTH, SCOPE_HEIGHT, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, MAX_AMP)

# visualizer still lags behind by small amounts - will investigate further
# current theory is that clock tick lags a bit while music plays uninterrupted
while total_elapsed * smp_per_second + WINDOW_SIZE < NUM_SAMPLES and RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if pause:
                    pygame.mixer.music.unpause()
                else: pygame.mixer.music.pause()
                pause = not pause
            elif event.key == pygame.K_q:
                RUNNING = False
            elif event.key == pygame.K_r:
                RECORDING = not RECORDING
        elif event.type == pygame.MOUSEBUTTONUP:
            print(mouse, gravitation)
            mouse_down = False
        elif event.type == pygame.MOUSEMOTION:
            mouse = event.pos

    if pause: 
        # reset the clock so the visualizer does not fall out of sync
        clock = pygame.time.Clock()
        continue

    elapsed = clock.tick(FPS)
    total_elapsed += elapsed

    if mouse_down:
        gravitation += elapsed
    else:
        gravitation -= elapsed
    gravitation = max(0, gravitation)


    # draw stuff
    screen.fill(pygame.Color(0, 0, 0))

    # draw the dotted line in the center
    # for i in range(0, SCREEN_HEIGHT, 20):
    #     pygame.draw.line(screen, pygame.Color(100, 100, 100), 
    #     (SCREEN_WIDTH / 2, i), (SCREEN_WIDTH / 2, i + 5), 3)

    # calculate the frame data
    window = avg_sample[total_elapsed * smp_per_second : total_elapsed * smp_per_second + WINDOW_SIZE]
    left_win = left_samples[total_elapsed * smp_per_second : total_elapsed * smp_per_second + WINDOW_SIZE]
    right_win = right_samples[total_elapsed * smp_per_second : total_elapsed * smp_per_second + WINDOW_SIZE]
    
    window_rms = rms(window)
    rms_prop = window_rms / MAX_AMP
    
    # add and draw the stars, nebula
    if (window_rms > random.randint(0, MAX_AMP) ** 0.9 and len(stars) < MAX_STARS):
        stars.add(
            Star(screen, rms_prop, 
                random.randint(0, SCREEN_WIDTH - 50), 
                random.randint(0, SCREEN_HEIGHT - 50)))
    
    neb_ctdown -= elapsed * rms_prop + .2
    if (neb_ctdown <= 0 and window_rms > random.randint(0, MAX_AMP) ** 1.5):
        neb_ctdown = MAX_NEB_CTDOWN
        nebulae.add(Nebula(screen, 
        random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100), 
        rms_prop, rand_color(50)))

    stars.update(elapsed, rms_prop* STAR_DECAY)
    nebulae.update(elapsed, rms_prop)
    for star in stars:
        star.draw()
    for neb in nebulae:
        neb.draw()

    oscope.draw(window)
    vscope.draw(left_win, right_win, 10)

    pygame.display.flip()

    if RECORDING:
        frame += 1
        screens.append(screen.copy())

pygame.mixer.quit()

print(len(screens))
for i, screen in enumerate(screens):
    print(f"Processing frame {i} of {len(screens)}")
    pygame.image.save(screen, f"imgs/frame{i}.png")