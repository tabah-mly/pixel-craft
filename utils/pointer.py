import pygame


class Pointer:
    def __init__(self, orbit_radius=20, offset=(0, 0)):
        self.orbit_radius = orbit_radius
        self.offset = pygame.Vector2(offset)

        self.arrow_length = 5
        self.arrow_width = 5
        self.arrow_points = [
            pygame.Vector2(self.arrow_length, 0),
            pygame.Vector2(-self.arrow_length, self.arrow_width),
            pygame.Vector2(-self.arrow_length, -self.arrow_width),
        ]

    def draw(self, surface, base_center, facing_right, camera):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_x, mouse_y)

        offset_x = self.offset.x if facing_right else -self.offset.x
        orbit_center = base_center + pygame.Vector2(offset_x, self.offset.y)

        direction = mouse_pos - orbit_center
        if direction.length() == 0:
            return

        direction = direction.normalize()

        pointer_pos = orbit_center + direction * self.orbit_radius
        angle = direction.as_polar()[1]

        final_points = [p.rotate(angle) + pointer_pos for p in self.arrow_points]

        self.pointer_pos = pointer_pos + camera.offset
        self.direction = direction

        pygame.draw.polygon(surface, (255, 255, 255), final_points)
