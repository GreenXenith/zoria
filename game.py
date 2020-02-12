import pygame
import os
from pygame.locals import *
from player import Player

# Init
pygame.init()
pygame.font.init()

# Screen Init (this is hacky .. going to implement a display module later to handle maximizing)
display = pygame.display.Info()
winsize = [display.current_w, display.current_h - 20]

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (display.current_w / 2, display.current_h)
os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pygame.display.set_mode(winsize, RESIZABLE)

# Constants
SCALE = 4

# Textures
textures = {
    "STONE": "tile.png",
    "CHARACTER": "character.png"
}

for name in textures:
    textures[name] = pygame.image.load("textures/" + textures[name])

# Map
tilemap = [
    ["STONE", "STONE", "STONE", "STONE", "STONE", "STONE"],
    ["STONE", "STONE", "STONE", "STONE", "STONE", "STONE"],
    ["STONE", "STONE", "STONE", "STONE", "STONE", "STONE"],
    ["STONE", "STONE", "STONE", "STONE", "STONE", "STONE"],
    ["STONE", "STONE", "STONE", "STONE", "STONE", "STONE"],
    ["STONE", "STONE", "STONE", "STONE", "STONE", "STONE"],
]

player = {
    "texture": textures["CHARACTER"],
    "rect": textures["CHARACTER"].get_rect()
}

test_player = Player()

# Mainloop
time = pygame.time.get_ticks()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    dtime = pygame.time.get_ticks() - time
    time = pygame.time.get_ticks()

    # rect = rect.move(speed[0] * dtime, speed[1] * dtime)
    # if rect.left < 0 or rect.right > width:
    #     speed[0] = -speed[0]
    # if rect.top < 0 or rect.bottom > height:
    #     speed[1] = -speed[1]

    screen.fill((0, 0, 0))

    for row in range(len(tilemap)):
        for column in range(len(tilemap[row])):
            texture = textures[tilemap[row][column]]
            tilesize = texture.get_rect().size[0]
            screen.blit(pygame.transform.scale(texture, (SCALE * tilesize, SCALE * tilesize)),
                        (column * SCALE * tilesize, row * SCALE * tilesize))


    keys = pygame.key.get_pressed()

    if keys[K_DOWN]:
        player["rect"].y = player["rect"].y + 10
    
    if keys[K_UP]:
        player["rect"].y = player["rect"].y - 10

    if keys[K_LEFT]:
        player["rect"].x = player["rect"].x - 10

    if keys[K_RIGHT]:
        player["rect"].x = player["rect"].x + 10 

    screen.blit(pygame.transform.scale(player["texture"], (SCALE * tilesize, SCALE * tilesize)), player["rect"])

    pygame.display.flip()
