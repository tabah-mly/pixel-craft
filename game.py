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

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.screen_event_listener(event)

    def update(self, dt):
        pass

    def draw(self):
        pass

    def start(self):
        while self.running:
            dt = self.set_fps(60)

            self.event_listener()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
