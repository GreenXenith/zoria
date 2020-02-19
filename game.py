import pygame

import os
import sys

import assets

# Init
pygame.init()
pygame.font.init()

# Screen Init (this is hacky .. going to implement a display module later to handle maximizing)
display = pygame.display.Info()
winsize = [display.current_w, display.current_h - 20]

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (display.current_w / 2, display.current_h)
os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pygame.display.set_mode(winsize, pygame.RESIZABLE)

# Constants
SCALE = 4

# Textures
textures = {
    "tile.png",
    "character.png"
}

for filename in textures:
    assets.load(filename)

# Map
STONE = "tile.png"

tilemap = [
    [STONE, STONE, STONE, STONE, STONE, STONE],
    [STONE, STONE, STONE, STONE, STONE, STONE],
    [STONE, STONE, STONE, STONE, STONE, STONE],
    [STONE, STONE, STONE, STONE, STONE, STONE],
    [STONE, STONE, STONE, STONE, STONE, STONE],
    [STONE, STONE, STONE, STONE, STONE, STONE],
]

# player = {
#     "texture": assets.get("character.png"),
#     "rect": assets.get("character.png").get_rect()
# }

from player import Player
player = Player("character.png")

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
            texture = assets.get(tilemap[row][column])
            tilesize = texture.get_rect().size[0]
            screen.blit(pygame.transform.scale(texture, (SCALE * tilesize, SCALE * tilesize)),
                        (column * SCALE * tilesize, row * SCALE * tilesize))


    keys = pygame.key.get_pressed()

    pos = player.get_pos()

    if keys[pygame.K_DOWN]:
        # player["rect"].y = player["rect"].y + 10
        player.set_pos(pos["x"], pos["y"] + 10)
    
    if keys[pygame.K_UP]:
        # player["rect"].y = player["rect"].y - 10
        player.set_pos(pos["x"], pos["y"] - 10)

    if keys[pygame.K_LEFT]:
        # player["rect"].x = player["rect"].x - 10
        player.set_pos(pos["x"] - 10, pos["y"])

    if keys[pygame.K_RIGHT]:
        # player["rect"].x = player["rect"].x + 10
        player.set_pos(pos["x"] + 10, pos["y"])

    screen.blit(pygame.transform.scale(player.sprite.texture, (SCALE * tilesize, SCALE * tilesize)), player.sprite.rect)

    pygame.display.flip()
