import pygame
import math, os, sys

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
player.sprite.set_rect((0, 16, 16, 24))
# TODO: Scale character up x2 (1.5m)
# TODO: Use asset loader for spritesheets
player.sprite.texture.set_animation(0, 0, 0)
player.set_pos(1.1, 1.1)
player.set_pos(map.generator.rooms[0].x + 2, map.generator.rooms[0].y + 2)

CENTER = [winsize[0] / 2, winsize[1] / 2]
BGCOLOR = pygame.Color("#3e1202")


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

    screen.fill(BGCOLOR)

    player.update(dtime, map)
    spritesheet.update(dtime)

    # Move the map based on player position
    psize = player.sprite.rect.size
    camera = [CENTER[0] - (psize[0] / 2 * SCALE), CENTER[1] - (psize[1] / 2 * SCALE)]

    for z in range(len(map.map)):
        for y in range(len(map.map[z])):
            for x in range(len(map.map[z][y])):
                if z == 1 and y == round(player.pos.y) and x == round(player.pos.x):
                    # Draw player
                    screen.blit(pygame.transform.scale(player.sprite.texture.frame, [round(SCALE * player.sprite.texture.width), round(SCALE * player.sprite.texture.height)]), camera)

                tile = map.get_tile(x, y, z)
                if tile:
                    # NOTE: Rotations are clockwise due to Y+ down rendering
                    # Will this break if there is no texture for the given rotation? Yes.
                    # Do I care? No.
                    texture = assets.get(tile.textures[tile.get_rotation()])

                    tilesize = texture.get_rect().size
                    scaledsize = [tilesize[0] * SCALE, tilesize[1] * SCALE]

                    tilex = (x * METER) - ((tilesize[0] / 2) - (METER / 2))
                    tiley = (y * METER) - (tilesize[1] - METER)

                    # TODO: Fix scaling gaps
                    pos = [
                        camera[0] + math.floor((tilex - (player.pos.x * METER)) * SCALE),
                        camera[1] + math.ceil((tiley - (player.pos.y * METER)) * SCALE)
                    ]

                    # Only render tile if on-screen
                    if pos[0] + scaledsize[0] >= 0 and pos[0] <= winsize[0] and \
                            pos[1] + scaledsize[1] >= 0 and pos[1] <= winsize[1]:
                        screen.blit(pygame.transform.scale(texture, [math.floor(scaledsize[0]), math.ceil(scaledsize[1])]), pos)

                # DEBUG
                # text = arial.render(str(int(x)) + ", " + str(int(y)), False, (255, 255, 255))
                # screen.blit(text, [x * 64 - (player.pos.x * round(SCALE * METER)) + camera[0], y * 64 - (player.pos.y * round(SCALE * METER)) + camera[1]])

    pygame.display.update()
    # pygame.display.flip()
