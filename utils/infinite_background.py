import pygame


class InfiniteBackground:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert()
        self.w, self.h = self.image.get_size()

    def draw(self, surface, camera):
        start_x = -camera.x % self.w
        start_y = -camera.y % self.h

        sw, sh = surface.get_size()

        for x in range(-self.w, sw + self.w, self.w):
            for y in range(-self.h, sh + self.h, self.h):
                surface.blit(self.image, (x + start_x, y + start_y))
