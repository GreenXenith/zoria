import pygame
import math

spritesheets = []

class SpriteSheet():
    file = ""

    start = 0
    end = 0

    speed = 0
    clock = 0

    frames = []
    frame_total = 0

    frame_index = None
    frame = None

    def __init__(self, filename, frameWidth, frameHeight = None):
        self.file = filename

        frameHeight = frameHeight or frameWidth

        img = pygame.image.load(filename)

        width = img.get_width()
        height = img.get_height()

        xframes = math.floor(width / frameWidth)
        yframes = math.floor(height / frameHeight)

        total = xframes * yframes

        x = 0
        y = 0
        for _ in range(total):
            surface = pygame.Surface((frameWidth, frameHeight), pygame.SRCALPHA, 32)
            surface.blit(img, (0, 0), (frameWidth * x, frameHeight * y, width, height))
            self.frames.append(surface.copy())

            x = (x + 1) % xframes
            if x % xframes == 0:
                y += 1

        self.width = frameWidth
        self.height = frameHeight

        self.xframes = xframes
        self.yframes = yframes
        self.frame_total = total

        self.frame_index = 0
        self.frame = self.frames[self.frame_index]

        self.start = 0
        self.end = total - 1
        self.speed = 0.05

        spritesheets.append(self)

    def minmax(self, frame):
        return min(max(0, frame), self.xframes * self.yframes - 1)

    def set_animation(self, start, end, speed):
        if self.start == start and self.end == end:
            return
        self.start = self.minmax(start)
        self.end = self.minmax(end)
        self.speed = max(0, speed)

        self.frame_index = self.start
        self.frame = self.frames[self.frame_index]

        self.clock = 0

    def update(self, dtime):
        self.clock += dtime
        if self.clock >= self.speed:
            self.clock = self.clock - self.speed

            self.frame_index = max(self.start, (self.frame_index + 1) % (self.end + 1))
            self.frame = self.frames[self.frame_index]

def update(dtime):
    for spritesheet in spritesheets:
        spritesheet.update(dtime)
