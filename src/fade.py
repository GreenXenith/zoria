import pygame

class Fade():
    def __init__(self, start, rate):
        rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
        self.alpha = start
        self.rate = rate
        self.text = ""

    def update(self, surface, dtime):
        self.alpha = max(0, min(self.alpha + int(self.rate * dtime), 255))
        if self.alpha >= 0:
            rect = pygame.display.get_surface().get_rect()
            self.image = pygame.transform.scale(self.image, rect.size)
            self.image.fill((0, 0, 0, self.alpha))
            surface.blit(self.image, (0, 0))

            text = pygame.font.SysFont("Times New Roman", round(rect.width / 16)).render(self.text, True, (255, 255, 255))
            alphasurf = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            alphasurf.fill((255, 255, 255, self.alpha))
            text.blit(alphasurf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(text, (rect.width / 2 - text.get_rect().width / 2, rect.height / 2 - text.get_rect().height / 2))



