import pygame
import math, os, sys

# Init
pygame.init()
pygame.font.init()

winsize = [800, 600]
screen = pygame.display.set_mode(winsize, pygame.RESIZABLE)

# Load all assets
from . import assets
for filename in os.listdir(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "assets")):
    assets.load(filename)

pygame.display.set_caption("Zoria")
pygame.display.set_icon(assets.load("icon.png"))

# Constants
SCALE = 2
METER = 32
FPS = 60

from . import controller, fade, register, spritesheet, vector
from .map import Map
from .player import Player

# Map
map = Map(METER)
map.generate(0)

# Player
player = Player(spritesheet.SpriteSheet(assets.get("character.png"), 32, 48), pygame.Rect(8, 32, 16, 16))
# TODO: Use asset loader for spritesheets
player.texture.set_animation(0, 0, 0)
mroom = map.generators[0].rooms[int(math.ceil(len(map.generators[0].rooms) / 2))]
player.set_pos(mroom.cx, mroom.cy)

CENTER = [winsize[0] / 2, winsize[1] / 2]
BGCOLOR = pygame.Color("#2d1003")

# Fade from/to black
player.fade = fade.Fade(255, -96)

def get_screenpos(x, y):
    return [
        camera[0] + round((x * METER - (player.pos.x * METER)) * SCALE),
        camera[1] + round((y * METER - (player.pos.y * METER)) * SCALE)
    ]

# Mainloop
clock = pygame.time.Clock()
while 1:
    dtime = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.VIDEORESIZE: # This is currently broken on Linux (SDL2)
            winsize = event.size
            SCALE = 2 * (winsize[0] / 800)
            CENTER = [winsize[0] / 2, winsize[1] / 2]
            screen = pygame.display.set_mode(winsize, pygame.RESIZABLE)

    screen.fill(BGCOLOR)

    player.update(dtime, map)
    spritesheet.update(dtime)

    # Move the map based on player position
    psize = player.rect.size
    camera = [int(CENTER[0] - (psize[0] / 2 * SCALE)), int(CENTER[1] - (psize[1] / 2 * SCALE))]

    player_rendered = False

    # Render loops
    for z in range(player.z - 1, player.z + 1):
        if z < len(map.map):
            for y in range(len(map.map[z])):
                for x in range(len(map.map[z][y])):
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

                        pos = get_screenpos(tilex / METER, tiley / METER)

                        # Only render tile if on-screen
                        if pos[0] + scaledsize[0] >= 0 and pos[0] <= winsize[0] and \
                                pos[1] + scaledsize[1] >= 0 and pos[1] <= winsize[1]:
                            tile.on_step(dtime, map, player)
                            screen.blit(pygame.transform.scale(texture, [round(scaledsize[0]) + 1, round(scaledsize[1]) + 1]), pos)

                    if not player_rendered and z == player.z and y == math.ceil(player.pos.y + 1 + player.rect[3] / METER):
                        # Draw player
                        screen.blit(pygame.transform.scale(player.texture.frame, [round(SCALE * player.texture.width), round(SCALE * player.texture.height)]), camera)
                        player_rendered = True

                # Draw sprites
                if z < len(map.sprites):
                    for sprite in map.sprites[z]:
                        if y == math.ceil(sprite.pos.y):
                            # Do on_step within 10 meter radius
                            if vector.distance(sprite.pos, player.pos) <= 10:
                                sprite.on_step(dtime, map, player)

                            # Only render if on-screen
                            scaledsize = [round(SCALE * sprite.texture.width), round(SCALE * sprite.texture.height)]
                            pos = get_screenpos(sprite.pos.x, sprite.pos.y)
                            if pos[0] + scaledsize[0] >= 0 and pos[0] <= winsize[0] and \
                                    pos[1] + scaledsize[1] >= 0 and pos[1] <= winsize[1]:
                                screen.blit(pygame.transform.rotate(pygame.transform.scale(sprite.texture.frame, scaledsize), sprite.rot), pos)

    player.hud.render(screen, SCALE)
    player.fade.update(screen, dtime)

    pygame.display.update()
