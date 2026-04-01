import pygame, sys, random
from player import Player
from utils.camera import Camera
from utils.infinite_background import InfiniteBackground

class Game:
    def __init__(self, width, height, title):
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title)

        self.running = True

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        pass

    def draw(self):
        pass

    def start(self):
        while self.running:
            dt = self.clock.tick(60)

            self.event_listener()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()