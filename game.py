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

import controller
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

    # Handle controls _before_ drawing
    pos = player.get_pos()

    if controller.is_down("up"):
        player.set_pos(pos["x"], pos["y"] - 10 * dtime)

    if controller.is_down("down"):
        player.set_pos(pos["x"], pos["y"] + 10 * dtime)

    if controller.is_down("left"):
        player.set_pos(pos["x"] - 10 * dtime, pos["y"])

    if controller.is_down("right"):
        player.set_pos(pos["x"] + 10 * dtime, pos["y"])

    # Draw the map based on player position
    pos = player.get_pos()
    print(pos)
    for row in range(len(tilemap)):
        for column in range(len(tilemap[row])):
            texture = assets.get(tilemap[row][column])
            tilesize = texture.get_rect().size[0]
            screen.blit(pygame.transform.scale(texture, (SCALE * tilesize, SCALE * tilesize)),
                        (column * SCALE * tilesize - pos["x"], row * SCALE * tilesize - pos["y"]))

    # Draw player in center of screen
    size = player.sprite.texture.get_rect().size
    screen.blit(pygame.transform.scale(player.sprite.texture, (SCALE * tilesize, SCALE * tilesize)), [display.current_w / 2 - (size[0] / 2 * SCALE), display.current_h / 2 - (size[1] / 2 * SCALE)])

    pygame.display.flip()
