import pygame

global assets
assets = {}

none = pygame.image.load("none.png")

def load(filename):
    assets[filename] = pygame.image.load("assets/" + filename) #.convert()
    return assets[filename]

def get(filename):
    try:
        return assets[filename]
    except:
        return none
