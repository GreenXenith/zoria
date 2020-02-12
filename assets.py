import pygame

global assets
assets = {}

def load(filename):
    assets[filename] = pygame.image.load("textures/" + filename)

def get(filename):
    return assets[filename]
