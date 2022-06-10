import pygame

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
        pass

    def samples_to_hsla(samples: list) -> pygame.Color:
        color: pygame.Color = pygame.Color(0, 0, 0)
        window = signal.windows.blackmanharris(10000)

        resample = signal.resample(samples, 10000)
        chunk_fft = np.abs(scipy.fft.fft(np.multiply(resample, window)))
        freq = np.argmax(chunk_fft[1:]) + 1

        if freq > 10000 or freq < 24:
            return color

        # formula adapted from https://en.wikipedia.org/wiki/Piano_key_frequencies
        hue: int = math.ceil(41.9 * math.log(freq / 440, 2) + 171.11)
        # saturation = rms(samples)
