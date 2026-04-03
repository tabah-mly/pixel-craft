import pygame


class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def follow(self, target_rect):
        self.offset.x = target_rect.centerx - self.width // 2
        self.offset.y = target_rect.centery - self.height // 2

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)
