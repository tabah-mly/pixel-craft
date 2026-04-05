import pygame, math


class Attack:
    def __init__(self, offset=(0, 8)):
        self.color = (255, 255, 255)
        self.angle = 0
        self.offset = pygame.Vector2(offset)

        self.progress = 0
        self.duration = 0.15
        self.active = False

        # this can be changed based on player stats
        self.hit_radius = 60  # how big the attack size
        self.hit_range = 80  # how far the attack travel

        self.hit_pos = pygame.Vector2(0, 0)
        self.has_hit = False
        self.hit_targets = set()

        self.is_debug = False

    def start(self):
        self.progress = 0
        self.active = True
        self.hit_targets.clear()

        surface = pygame.display.get_surface()
        center = pygame.Vector2(surface.get_width() // 2, surface.get_height() // 2)

        mx, my = pygame.mouse.get_pos()
        vec = pygame.Vector2(mx, my) - center

        if vec.length_squared() == 0:
            vec = pygame.Vector2(0, -1)

        self.direction = vec.normalize()
        self.base_angle = vec.angle_to(pygame.Vector2(0, -1))

    def draw_cres(self, surface, t, pos=(0, 0), size=(100, 150), angle=0):
        w, h = size
        x, y = pygame.Vector2(pos) - self.offset

        attack_surface = pygame.Surface((w, 200), pygame.SRCALPHA)

        pygame.draw.ellipse(attack_surface, (self.color), (0, 0, w, h))
        pygame.draw.ellipse(attack_surface, (0, 255, 0, 0), (0, (w / 2), w, h))

        rotated = pygame.transform.rotate(attack_surface, angle)
        rotated_rect = rotated.get_rect(center=(x, y))
        surface.blit(rotated, rotated_rect)

    def update(self, dt):
        if not self.active:
            return

        self.progress += dt / self.duration

        if self.progress >= 1:
            self.progress = 1
            self.active = False

        # reset hit each frame
        self.has_hit = False

        # only allow hit near peak
        if 0.2 < self.progress < 0.8:
            self.has_hit = True

    def map_size(self):
        min_radius, max_radius = 40, 100
        self.hit_radius = max(min_radius, min(max_radius, self.hit_radius))
        return round(
            1 + (self.hit_radius - min_radius) / 4
        )  # This should return from 1 to 16 (int) based on hit_radius

    def draw(self, surface, camera, player_pos):
        if not self.active:
            return

        center = player_pos
        t = self.progress

        curve = (t**2) * (1 - t)  # growth curve
        base = 1.3 * ((1 - t) ** 2)  # decay base

        raw_scale = base + curve * self.map_size()

        min_scale = 0.5  # prevent too small
        scale = min_scale + raw_scale * (1 - min_scale)

        # movement
        distance = self.hit_range * (1 - (1 - t) ** 2) - 60
        world_pos = center + self.direction * distance
        forward_offset = self.direction * 60
        self.hit_pos = world_pos + forward_offset

        screen_pos = world_pos - camera.offset
        size = (int(120 * scale), int(160 * scale))

        self.draw_cres(surface, t, screen_pos, size=size, angle=self.base_angle)
        if self.is_debug:
            debug_pos = self.hit_pos - camera.offset
            pygame.draw.circle(surface, (255, 0, 0, 100), debug_pos, self.hit_radius, 2)
