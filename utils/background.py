import pygame


class InfiniteBackground:
    def __init__(self, image_path, scale=1, repeat_x=True, repeat_y=True):
        original = pygame.image.load(image_path).convert()

        self.image = pygame.transform.scale(
            original, (original.get_width() * scale, original.get_height() * scale)
        )

        self.w = self.image.get_width()
        self.h = self.image.get_height()

        self.repeat_x = repeat_x
        self.repeat_y = repeat_y

    def draw(self, surface, camera_offset):
        screen_w, screen_h = surface.get_size()

        if self.repeat_x:
            start_x = int(camera_offset.x // self.w) - 1
            end_x = start_x + screen_w // self.w + 3
        else:
            start_x = end_x = 0

        if self.repeat_y:
            start_y = int(camera_offset.y // self.h) - 1
            end_y = start_y + screen_h // self.h + 3
        else:
            start_y = end_y = 0

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                pos_x = x * self.w - camera_offset.x
                pos_y = y * self.h - camera_offset.y
                surface.blit(self.image, (pos_x, pos_y))
