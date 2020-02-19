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

# Screen Init (this is hacky .. going to implement a display module later to handle maximizing)
display = pygame.display.Info()
winsize = [display.current_w, display.current_h - 20]

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (display.current_w / 2, display.current_h)
os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pygame.display.set_mode(winsize, pygame.RESIZABLE)

# Textures
textures = {
    "floor_cobble.png",
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
player.set_pos(1 * 32 * SCALE, 1 * 32 * SCALE)

CENTER = [display.current_w / 2, display.current_h / 2]

# Mainloop
clock = pygame.time.Clock()
while 1:
    dtime = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # rect = rect.move(speed[0] * dtime, speed[1] * dtime)
    # if rect.left < 0 or rect.right > width:
    #     speed[0] = -speed[0]
    # if rect.top < 0 or rect.bottom > height:
    #     speed[1] = -speed[1]

    screen.fill((0, 0, 0))

    # Handle controls _before_ drawing
    pos = player.get_pos()

    if controller.is_down("up"):
        newy = pos["y"] - player.speed * SCALE * METER * dtime
        player.set_pos(pos["x"], newy)

    if controller.is_down("down"):
        newy = pos["y"] + player.speed * SCALE * METER * dtime
        player.set_pos(pos["x"], newy)

    if controller.is_down("left"):
        newx = pos["x"] - player.speed * SCALE * METER * dtime
        player.set_pos(newx, pos["y"])

    if controller.is_down("right"):
        newx = pos["x"] + player.speed * SCALE * METER * dtime
        player.set_pos(newx, pos["y"])

    # Move the map based on player position
    pos = player.get_pos()
    psize = player.sprite.texture.get_rect().size

    camera = [CENTER[0] - (psize[0] / 2 * SCALE), CENTER[1] - (psize[1] / 2 * SCALE)]

    for row in range(len(tilemap)):
        for column in range(len(tilemap[row])):
            texture = assets.get(map.map["tiles"][tilemap[row][column]]["texture"])
            tilesize = texture.get_rect().size[0]
            screen.blit(pygame.transform.scale(texture, (SCALE * tilesize, SCALE * tilesize)), (column * SCALE * tilesize - pos["x"] + camera[0], row * SCALE * tilesize - pos["y"] + camera[1]))

    # Draw player based on camera position
    screen.blit(pygame.transform.scale(player.sprite.texture, (SCALE * tilesize, SCALE * tilesize)), camera)

    pygame.display.flip()
