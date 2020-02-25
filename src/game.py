import pygame
import os
import sys
from . import assets, controller, spritesheet
from .map import Map
from .player import Player

# Constants
SCALE = 4
METER = 32
FPS = 60

# Init
pygame.init()
pygame.font.init()

# Screen Init (might implement a display module later to handle maximizing)
pygame.display.set_caption("Zoria")
pygame.display.set_icon(assets.load("icon.png"))
winsize = [800, 600]
screen = pygame.display.set_mode(winsize) #, pygame.RESIZABLE)

# Load all assets
for filename in os.listdir(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "assets")):
    assets.load(filename)

# Map
map = Map(METER)
map.load("map.json")

# Player
player = Player()
player.sprite.texture = spritesheet.SpriteSheet(assets.get("character.png"), 16, 24)
player.sprite.set_rect((0, 0, 16, 24))
# TODO: Use asset loader for spritesheets
player.sprite.texture.set_animation(0, 0, 0)
player.set_pos(1.1, 1.1)

CENTER = [winsize[0] / 2, winsize[1] / 2]

# Mainloop
clock = pygame.time.Clock()
while 1:
    dtime = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0, 0, 0))

    player.update(dtime, map)
    spritesheet.update(dtime)

    # Move the map based on player position
    psize = player.sprite.rect.size
    camera = [CENTER[0] - (psize[0] / 2 * SCALE), CENTER[1] - (psize[1] / 2 * SCALE)]

    for layer in map.map["renderLayers"]:
        for row in range(len(layer)):
            for column in range(len(layer[row])):
                materialIndex = layer[row][column]
                if materialIndex != 0:
                    texture = assets.get(map.map["tiles"][materialIndex - 1])
                    tilesize = texture.get_rect().size[0]
                    screen.blit(pygame.transform.scale(texture, [SCALE * tilesize, SCALE * tilesize]), [
                            column * SCALE * tilesize - (player.pos.x * SCALE * METER) + camera[0],
                            row * SCALE * tilesize - (player.pos.y * SCALE * METER) + camera[1]
                        ])

    # Draw player based on camera position
    screen.blit(pygame.transform.scale(player.sprite.texture.frame, [SCALE * player.sprite.texture.width, SCALE * player.sprite.texture.height]), camera)

    pygame.display.flip()
