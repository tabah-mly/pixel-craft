import pygame, sys
from player import Player
from utils.game_base import GameBase


class Game(GameBase):
    def __init__(self, width, height, title):
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.running = True
        self.game_state = "playing"

        self.initialize_object()

        # Entities
        self.player = Player(width // 2, height // 2, self.pointer)
        self.enemies = []
        self.entities = [self.player] + self.enemies

        self.initialize_screen_time()

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.screen_event_listener(event)

    def update(self, dt):
        if self.update_screen(dt):
            return

        self.check_game_over()
        self.timer += dt
        self.update_entities(dt)
        self.camera.follow(self.player.rect)
        self.attack_logic()
        self.difficult_handler(dt)
        self.spawn_enemy(dt)
        self.update_coin(dt)
        self.clean_entities()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen, self.camera.offset)
        self.draw_coin()
        self.draw_entities()
        self.ui.draw(self.player, self.timer)
        self.pointer.draw(self.screen, self.camera)
        self.draw_screen()

    def start(self):
        while self.running:
            dt = self.set_fps(60)

            self.event_listener()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
