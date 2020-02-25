import pygame

global assets
assets = {}

def load(filename):
    assets[filename] = pygame.image.load("assets/" + filename)
    return assets[filename]

def get(filename):
    return assets[filename]
