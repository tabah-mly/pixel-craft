import pygame


class GameOver:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.fade_alpha = 0
        self.max_alpha = 200
        self.fade_speed = 200

        self.font_big = pygame.font.Font("assets/fonts/monogram.ttf", 120)
        self.font_small = pygame.font.Font("assets/fonts/monogram.ttf", 40)

        self.button_rect = pygame.Rect(0, 0, 200, 60)
        self.button_rect.center = (self.width // 2, self.height // 2 + 60)

        self.button_hover = False

    def handle_event(self, event):
        if self.fade_alpha < 150:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    return True
        return False

    def update(self, dt):
        self.fade_alpha = min(self.max_alpha, self.fade_alpha + self.fade_speed * dt)

        mouse_pos = pygame.mouse.get_pos()
        self.button_hover = self.button_rect.collidepoint(mouse_pos)

    def draw(self, surface):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(self.fade_alpha))
        surface.blit(overlay, (0, 0))
        if self.fade_alpha > 150:
            pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_HAND
                if self.button_hover
                else pygame.SYSTEM_CURSOR_ARROW
            )
            text = self.font_big.render("GAME OVER", True, (255, 0, 0))

            rect = text.get_rect(center=(self.width // 2, self.height // 2 - 30))

            surface.blit(text, rect)

            pygame.draw.rect(
                surface,
                (255, 255, 255),
                self.button_rect,
                0 if self.button_hover else 2,
            )
            color = (0, 0, 0, 0) if self.button_hover else (255, 255, 255)
            btn_text = self.font_small.render("restart", True, color)
            btn_rect = btn_text.get_rect(center=self.button_rect.center)
            surface.blit(btn_text, btn_rect)

    def reset(self):
        self.fade_alpha = 0
