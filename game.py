import pygame
import os
import sys
import assets

# Constants
SCALE = 4
METER = 32
FPS = 60

# Init
pygame.init()
pygame.font.init()

# Screen Init (might implement a display module later to handle maximizing)
display = pygame.display.Info()
winsize = [800, 600]

# os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (display.current_w / 2, display.current_h)
# os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pygame.display.set_mode(winsize) #, pygame.RESIZABLE)

# Textures (non-map only)
textures = {
    "character.png"
}

for filename in textures:
    assets.load(filename)

# Map
from map import Map
map = Map()
map.load("map.json")

tilemap = map.map["map"]

import controller
from player import Player
player = Player("character.png")
player.sprite.set_rect(player.sprite.texture.get_rect())
player.set_pos(1, 1)

CENTER = [winsize[0] / 2, winsize[1] / 2]

# Mainloop
clock = pygame.time.Clock()
while 1:
    dtime = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0, 0, 0))

    player.update(dtime, map)

    # Move the map based on player position
    pos = player.get_pos()
    psize = player.sprite.texture.get_rect().size
    camera = [CENTER[0] - (psize[0] / 2 * SCALE), CENTER[1] - (psize[1] / 2 * SCALE)]

    for row in range(len(tilemap)):
        for column in range(len(tilemap[row])):
            texture = assets.get(map.map["tiles"][tilemap[row][column]]["texture"])
            tilesize = texture.get_rect().size[0]
            screen.blit(pygame.transform.scale(texture, [SCALE * tilesize, SCALE * tilesize]), [
                    column * SCALE * tilesize - (pos["x"] * SCALE * METER) + camera[0],
                    row * SCALE * tilesize - (pos["y"] * SCALE * METER) + camera[1]
                ])

    # Draw player based on camera position
    screen.blit(pygame.transform.scale(player.sprite.texture, [SCALE * tilesize, SCALE * tilesize]), camera)

    pygame.display.flip()
