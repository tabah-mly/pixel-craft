import pygame


class UpgradeMenu:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font("assets/fonts/monogram.ttf", 40)

        self.options = [
            {
                "text": "Heal          ",
                "key": "hp",
                "increment": 10,
                "base_cost": 10,
                "cost": 10,
                "level": 0,
                "icon": "assets/imgs/heal.png",
            },
            {
                "text": "Max HP    ",
                "key": "max_hp",
                "increment": 10,
                "base_cost": 50,
                "cost": 50,
                "level": 1,
                "icon": "assets/imgs/health.png",
            },
            {
                "text": "Speed     ",
                "key": "speed",
                "increment": 5,
                "base_cost": 10,
                "cost": 10,
                "level": 1,
                "icon": "assets/imgs/speed.png",
            },
            {
                "text": "Strength  ",
                "key": "damage",
                "increment": 5,
                "base_cost": 10,
                "cost": 10,
                "level": 1,
                "icon": "assets/imgs/strength.png",
            },
            {
                "text": "Knockback ",
                "key": "knockback",
                "increment": 5,
                "base_cost": 10,
                "cost": 10,
                "level": 1,
                "icon": "assets/imgs/knockback.png",
            },
            {
                "text": "Stun      ",
                "key": "stun",
                "increment": 0.1,
                "base_cost": 10,
                "cost": 10,
                "level": 1,
                "icon": "assets/imgs/stun.png",
            },
        ]

        for item in self.options:
            item["image"] = pygame.image.load(item["icon"]).convert_alpha()

        self.button = pygame.image.load("assets/imgs/button.png").convert_alpha()
        self.panel_image = pygame.image.load("assets/imgs/panel.png").convert_alpha()

    def handle_upgrade(self, index):
        player_stats = self.player.stats
        player_items = self.player.items
        option = self.options[index]

        if player_items["coin"] < option["cost"]:
            return

        stats_key = option["key"]

        if stats_key == "hp":
            if player_stats["hp"] >= player_stats["max_hp"]:
                return
            val = player_stats["hp"] + option["increment"]
            player_stats["hp"] = min(val, player_stats["max_hp"])
        else:
            player_stats[stats_key] += option["increment"]
            option["level"] += 1
            option["cost"] = option["level"] * option["base_cost"]

        self.player.items["coin"] -= option["cost"]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mx, my):
                    self.handle_upgrade(i)

    def surface_button(self, icon_image, text, scale=2, padding=10):
        # background
        bw, bh = self.button.get_size()
        bg = pygame.transform.scale(self.button, (int(bw * scale), int(bh * scale)))

        # icon
        iw, ih = icon_image.get_size()
        icon = pygame.transform.scale(icon_image, (int(iw * scale), int(ih * scale)))

        # text
        text_surface = self.font.render(text, True, (255, 255, 255))

        # compose
        surface = bg.copy()

        center_y = bg.get_height() // 2
        content_x = 30

        icon_rect = icon.get_rect(midleft=(content_x, center_y))
        text_rect = text_surface.get_rect(midleft=(icon_rect.right + padding, center_y))

        surface.blit(icon, icon_rect)
        surface.blit(text_surface, text_rect)

        return surface

    def update(self, dt):
        pass

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        center_screen = screen_width // 2, screen_height // 2

        surfaces = []
        rects = []

        start_y = 0
        row_spacing = 120
        col_spacing = 225

        for i, item in enumerate(self.options):
            level = self.options[i]["level"]
            cost = self.options[i]["cost"]
            level_text = f"Lv{level} " if level else ""
            surface = self.surface_button(
                item["image"], f"{level_text}{item["text"]} C{cost}"
            )

            col, row = i % 2, i // 2
            x = -col_spacing if col == 0 else col_spacing
            y = start_y + row * row_spacing

            rect = surface.get_rect(center=(x, y))

            surfaces.append(surface)
            rects.append(rect)

        container_rect = rects[0].copy()
        for r in rects[1:]:
            container_rect.union_ip(r)

        offset = center_screen - pygame.Vector2(container_rect.center)

        padding = 60  # space around buttons

        panel_width = container_rect.width + padding * 2
        panel_height = container_rect.height + padding * 2

        panel = pygame.transform.scale(
            self.panel_image, (int(panel_width), int(panel_height))
        )

        panel_rect = panel.get_rect(center=center_screen)
        screen.blit(panel, panel_rect)

        self.option_rects = []
        hovering_any = False
        mx, my = pygame.mouse.get_pos()

        for surface, rect in zip(surfaces, rects):
            final_rect = rect.move(offset)
            screen.blit(surface, final_rect)

            if final_rect.collidepoint(mx, my):
                hovering_any = True
                pygame.draw.rect(screen, (230, 69, 57), final_rect, 4)

            self.option_rects.append(final_rect)

        if hovering_any:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
