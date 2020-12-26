# random.randint wrapper
import random

def rand(*args):
    random.seed()
    return random.randint(*args)
