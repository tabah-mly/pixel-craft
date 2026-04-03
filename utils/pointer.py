import pygame


class Pointer:
    def __init__(self, orbit_radius=75, offset=(0, 8), debug=False):
        self.is_active = True
        self.orbit_radius = orbit_radius
        self.offset = pygame.Vector2(offset)
        self.pointer_length = 14
        self.pointer_width = 10
        self.debug = debug
        self.direction = pygame.Vector2(0, 0)
        self.ranged = True
        self.cursor_radius = 10

    def draw(self, surface, camera):
        if not self.is_active:
            return
        pygame.mouse.set_visible(not self.is_active)
        mouse_pos = pygame.mouse.get_pos()
        center_sreen = (
            pygame.Vector2(surface.get_width() // 2, surface.get_height() // 2)
            - self.offset
        )

        vec = mouse_pos - center_sreen
        self.direction = vec.normalize() if vec.length_squared() > 0 else self.direction
        anchor_point = center_sreen + self.direction * self.orbit_radius
        B = anchor_point - self.direction * self.pointer_length

        perp = pygame.Vector2(-self.direction.y, self.direction.x)

        R1 = B + perp * self.pointer_width
        R2 = B - perp * self.pointer_width

        if self.debug:
            # center
            pygame.draw.circle(surface, (0, 0, 255), center_sreen, 5)

            # orbit
            pygame.draw.circle(surface, (0, 255, 0), center_sreen, self.orbit_radius, 2)

            pygame.draw.circle(
                surface,
                (0, 255, 0),
                center_sreen,
                self.orbit_radius - self.pointer_length,
                2,
            )

            # cursor
            pygame.draw.circle(surface, (0, 0, 255), mouse_pos, 5)

            # line
            pygame.draw.line(surface, (0, 0, 255), center_sreen, mouse_pos, 2)

            # point
            pygame.draw.circle(surface, (255, 0, 0), anchor_point, 3)

            # R1
            pygame.draw.circle(surface, (255, 0, 0), R1, 3)

            # R2
            pygame.draw.circle(surface, (255, 0, 0), R2, 3)

        # pointer
        pygame.draw.polygon(surface, (255, 255, 255), (anchor_point, R1, R2))

        # cursor
        pygame.draw.circle(surface, (255, 255, 255), mouse_pos, self.cursor_radius, 2)
        if self.ranged:
            line_width = 2
            half_line_width = line_width // 2
            line_height = self.cursor_radius * 1.5
            pygame.draw.line(
                surface,
                (255, 255, 255),
                (
                    mouse_pos[0] - half_line_width,
                    mouse_pos[1] - line_height - half_line_width,
                ),
                (
                    mouse_pos[0] - half_line_width,
                    mouse_pos[1] + line_height,
                ),
                line_width,
            )
            pygame.draw.line(
                surface,
                (255, 255, 255),
                (
                    mouse_pos[0] - line_height - half_line_width,
                    mouse_pos[1] - half_line_width,
                ),
                (
                    mouse_pos[0] + line_height,
                    mouse_pos[1] - half_line_width,
                ),
                line_width,
            )
