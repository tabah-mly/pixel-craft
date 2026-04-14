import pygame
from utils.spritesheet import SpriteSheet
from utils.player_base import PlayerBase


class Player(PlayerBase):
    def __init__(self, x, y, pointer):
        self.animations = {
            "idle": SpriteSheet("assets/imgs/player_idle.png", 4, 0.1),
            "walk": SpriteSheet("assets/imgs/player_walk.png", 4, 0.1),
        }

        self.initialize(x, y, pointer)

        self.stats = {
            "max_hp": 100,
            "hp": 100,
            "speed": 250,
            "damage": 20,
            "knockback": 20,
            "stun": 0,
        }

        self.items = {
            "coin": 0,
            "killed": 0,
        }

    def handle_input(self, dt):
        pass

    def update(self, dt):
        pass

    def draw(self, surface, camera):
        self.draw_sprites(surface, camera)
        