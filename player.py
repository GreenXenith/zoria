from sprite import Sprite

class Player:
    x = 0
    y = 0

    hp = 100
    mp = 50
    xp = 0

    sprite = Sprite()
    sprite.set_texture("character.png")