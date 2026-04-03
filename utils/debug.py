import pygame


class Debug:
    def __init__(self, screen, x=10, y=10, font_size=20):
        self.screen = screen
        self.x = x
        self.y = y
        self.start_y = y
        self.font_size = font_size
        self.font = pygame.font.SysFont("consolas", self.font_size)

        self.lines = []

    def add(self, label, value=None):
        if value is None:
            self.lines.append(str(label))
        else:
            self.lines.append(f"{label}: {value}")

    def render_text_outline(self, font, text, color, outline_color, outline_size=1):
        base = font.render(text, True, color)
        outline = font.render(text, True, outline_color)

        w = base.get_width() + outline_size * 2
        h = base.get_height() + outline_size * 2

        surface = pygame.Surface((w, h), pygame.SRCALPHA)

        for dx in range(-outline_size, outline_size + 1):
            for dy in range(-outline_size, outline_size + 1):
                if dx != 0 or dy != 0:
                    surface.blit(outline, (dx + outline_size, dy + outline_size))

        surface.blit(base, (outline_size, outline_size))

        return surface

    def show(self):
        y = self.start_y

        for line in self.lines:
            surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(surface, (self.x, y))
            y += self.font.get_height()

        self.lines.clear()

    def text(self, text, pos):
        surface = self.font.render(f"{text}", True, (255, 255, 255))
        text_rect = surface.get_rect(center=(pos[0], pos[1] - 45))
        self.screen.blit(surface, text_rect)
