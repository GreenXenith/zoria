# random.randint wrapper
import random
import time

def rand(*args):
    random.seed(time.clock())
    return random.randint(*args)
