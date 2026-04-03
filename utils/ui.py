import pygame


class Ui:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/monogram.ttf", 40)
        self.font_big = pygame.font.Font("assets/fonts/monogram.ttf", 60)

    def format_time(self, seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        ms = int((seconds % 1) * 100)  # 2-digit ms

        return f"{hrs:02}:{mins:02}:{secs:02}"

    def draw_image(self, path, pos, scale, align=-1):
        surface = pygame.image.load(path)
        surface_width, surface_height = surface.get_size()
        scaled_surface = surface_width * scale, surface_height * scale
        surface = pygame.transform.scale(surface, (scaled_surface))
        rect = surface.get_rect()
        if align < 0:
            rect.topleft = pos
        elif align > 0:
            rect.topright = pos
        else:
            rect.centerx = pos[0]

        self.screen.blit(surface, rect)
        return rect

    def draw_text(self, text, pos, font_big=False, align=-1):
        # align (-1 left, 0 center, 1 left)
        if font_big:
            surface = self.font_big.render(f"{text}", True, (255, 255, 255))
        else:
            surface = self.font.render(f"{text}", True, (255, 255, 255))
        rect = surface.get_rect()
        if align < 0:
            rect.topleft = pos
        elif align > 0:
            rect.topright = pos
        else:
            rect.centerx = pos[0]
        self.screen.blit(surface, rect)
        return rect

    def draw(self, player, timer):
        # hp
        hp_img = self.draw_image("assets/imgs/health.png", (10, 10), 2)
        self.draw_text(player.stats["hp"], (hp_img.x + hp_img.w + 10, 10))

        # coins
        coins_img = self.draw_image(
            "assets/imgs/coins.png", (10, hp_img.y + hp_img.h + 10), 2
        )
        self.draw_text(
            f"C{player.items["coin"]}", (coins_img.x + coins_img.w + 10, coins_img.y)
        )

        # kills
        kill_img = self.draw_image(
            "assets/imgs/skull.png", (self.screen.get_width() - 100, 10), 2, 1
        )
        self.draw_text(player.items["killed"], (kill_img.x + kill_img.w + 10, 10))

        # Timer
        self.draw_text(
            self.format_time(timer), (self.screen.get_width() // 2, 10), True, 0
        )
