import pygame
import os, sys

# Init
pygame.init()
pygame.font.init()

winsize = [800, 600]
screen = pygame.display.set_mode(winsize, pygame.RESIZABLE)

from . import assets, controller, register, spritesheet
from .map import Map
from .player import Player

pygame.display.set_caption("Zoria")
pygame.display.set_icon(assets.load("icon.png"))

# Constants
SCALE = 2
METER = 32
FPS = 60

# Load all assets
for filename in os.listdir(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "assets")):
    assets.load(filename)

# Map
map = Map(METER)
# map.load("map.json")
map.generate()

# Player
player = Player()
player.sprite.texture = spritesheet.SpriteSheet(assets.get("character.png"), 16, 24)
player.sprite.set_rect((0, 0, 16, 24))
# TODO: Use asset loader for spritesheets
player.sprite.texture.set_animation(0, 0, 0)
player.set_pos(1.1, 1.1)
player.set_pos(map.generator.rooms[0].x + 2, map.generator.rooms[0].y + 2)

CENTER = [winsize[0] / 2, winsize[1] / 2]

arial = pygame.font.SysFont("Arial", 10)

# Mainloop
clock = pygame.time.Clock()
while 1:
    dtime = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            winsize = event.size
            SCALE = 2 * (winsize[0] / 800)
            CENTER = [winsize[0] / 2, winsize[1] / 2]
            screen = pygame.display.set_mode(winsize, pygame.RESIZABLE)

    screen.fill((0, 0, 0))

    player.update(dtime, map)
    spritesheet.update(dtime)

    # Move the map based on player position
    psize = player.sprite.rect.size
    camera = [CENTER[0] - (psize[0] / 2 * SCALE), CENTER[1] - (psize[1] / 2 * SCALE)]

    for z in range(len(map.map)):
        for y in range(len(map.map[z])):
            for x in range(len(map.map[z][y])):
                tile = map.get_tile(x, y, z)
                if tile:
                    texture = assets.get(tile.texture)

                    # Rotations are clockwise due to Y+ down rendering
                    # NOTE: This will be obsolete once game is converted to 2.5D
                    rotated = pygame.transform.rotate(texture, -90 * tile.rotation)

                    tilesize = texture.get_rect().size

                    tilex = (x * METER) - ((tilesize[0] / 2) - (METER / 2))
                    tiley = (y * METER) - (tilesize[1] - METER)

                    pos = [
                        camera[0] + round((tilex - (player.pos.x * METER)) * SCALE),
                        camera[1] + round((tiley - (player.pos.y * METER)) * SCALE)
                    ]

                    # Only render tile if on-screen
                    if pos[0] + tilex >= 0 and pos[0] <= winsize[0] and \
                            pos[1] + tiley >= 0 and pos[1] <= winsize[1]:
                        screen.blit(pygame.transform.scale(rotated, [round(tilesize[0] * SCALE), round(tilesize[1] * SCALE)]), pos)

                # text = arial.render(str(int(x)) + ", " + str(int(y)), False, (255, 255, 255))
                # screen.blit(text, [x * 64 - (player.pos.x * round(SCALE * METER)) + camera[0], y * 64 - (player.pos.y * round(SCALE * METER)) + camera[1]])

    # Draw player based on camera position
    screen.blit(pygame.transform.scale(player.sprite.texture.frame, [round(SCALE * player.sprite.texture.width), round(SCALE * player.sprite.texture.height)]), camera)

    pygame.display.update()
    # pygame.display.flip()
