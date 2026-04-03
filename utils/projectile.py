import pygame


class Projectile:
    def __init__(self, pos, direction, player_speed, speed=500):
        self.pos = pygame.Vector2(pos)
        dir_vec = pygame.Vector2(direction)
        if dir_vec.length_squared() == 0:
            dir_vec = pygame.Vector2(1, 0)
        self.dir = dir_vec.normalize()
        self.speed = speed + player_speed
        self.radius = 6
        self.alive = True
        self.life = 0
        self.max_life = 2.0  # seconds

    def update(self, dt):
        self.pos += self.dir * self.speed * dt

        self.life += dt
        if self.life > self.max_life:
            self.alive = False

    def draw(self, surface, camera):
        screen_pos = self.pos - camera.offset
        pygame.draw.circle(surface, (255, 255, 255), screen_pos, self.radius)
