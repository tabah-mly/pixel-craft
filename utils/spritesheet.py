import pygame


class SpriteSheet:
    def __init__(self, sheet_path, scale=6, speed=200):
        self.speed = speed
        self.scale = scale

        self.sheet = pygame.image.load(sheet_path).convert_alpha()
        self.sheet_width, self.sheet_height = self.sheet.get_size()

        self.frame_count = self.sheet_width // self.sheet_height

        self.frames = []
        self._generate_frames()

        self.frame_index = 0
        self.image = self.frames[0]
        self.timer = 0

        self.masks = [pygame.mask.from_surface(frame) for frame in self.frames]

    def _generate_frames(self):
        for i in range(self.frame_count):
            frame = pygame.Surface(
                (self.sheet_height, self.sheet_height), pygame.SRCALPHA
            )

            frame.blit(
                self.sheet,
                (0, 0),
                (i * self.sheet_height, 0, self.sheet_height, self.sheet_height),
            )

            frame = pygame.transform.scale(
                frame, (self.sheet_height * self.scale, self.sheet_height * self.scale)
            )

            self.frames.append(frame)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.speed:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def reset(self):
        self.frame_index = 0
        self.timer = 0
        self.image = self.frames[0]
