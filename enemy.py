import pygame
from utils.spritesheet import SpriteSheet
from utils.enemy_base import EnemyBase


class Enemy(EnemyBase):
    def __init__(self, player, x, y, difficulty):
        self.animations = {
            "walk": SpriteSheet("assets/imgs/enemy_walk.png", 4, 0.1),
            "hit": SpriteSheet("assets/imgs/enemy_hit.png", 4, 0.1),
            "attack": SpriteSheet("assets/imgs/enemy_attack.png", 4, 0.1),
        }

        self.initialize(player, x, y)

        self.stats = {
            "max_hp": 100,
            "hp": 100,
            "damage": 5,
            "speed": 100,
            "attack_range": 50,
        }

        self.apply_difficulty(difficulty)

    def update(self, dt):
        if not self.is_alive():
            return

        self.animator.update(dt)

        if self.is_hit(dt):
            return

        self.move(dt)

    def draw(self, surface, camera):
        if not self.is_alive():
            return
        self.draw_sprites(surface, camera)
