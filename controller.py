import pygame

keybinds = {
    "up": ["w", "UP"],
    "down": ["s", "DOWN"],
    "left": ["a", "LEFT"],
    "right": ["d", "RIGHT"],
}

def is_down(control):
    keys = pygame.key.get_pressed()
    for key in keybinds[control]:
        if keys[getattr(pygame, "K_" + key)]:
            return True
