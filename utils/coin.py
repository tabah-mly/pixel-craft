import pygame, random
from utils.spritesheet import SpriteSheet


class Coin:
    def __init__(self, pos):
        self.animator = SpriteSheet("assets/imgs/coin.png", 2, 0.1)
        self.pos = pygame.Vector2(pos)
        self.rect = self.animator.image.get_rect(center=pos)

        self.alive = True
        self.value = random.randint(1, 5)

        self.pickup_radius = 20
        self.maget_radius = 50
        self.magnet_speed = 200

        self.lifetime = 5.0  # seconds
        self.timer = self.lifetime

    def update(self, dt, player):
        self.animator.update(dt)

        self.timer -= dt
        if self.timer <= 0:
            self.alive = False
            return

        direction = player.pos - self.pos
        distance = direction.length()

        if distance < self.maget_radius:
            if distance != 0:
                self.pos += direction.normalize() * self.magnet_speed * dt
                self.rect.center = self.pos

        if distance < self.pickup_radius:
            player.items["coin"] += self.value
            self.alive = False

    def draw(self, surface, camera):
        surface.blit(self.animator.image, camera.apply(self.rect))
