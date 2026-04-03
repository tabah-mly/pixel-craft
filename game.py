import pygame, sys, random, math
from player import Player
from enemy import Enemy
from utils.camera import Camera
from utils.background import InfiniteBackground
from utils.pointer import Pointer
from utils.coin import Coin
from utils.game_over import GameOver
from utils.upgrade_menu import UpgradeMenu
from utils.ui import Ui


class Game:
    def __init__(self, width, height, title):
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.running = True
        self.timer = 0
        self.game_state = "playing"

        # UI
        self.pointer = Pointer()
        self.camera = Camera(width, height)
        self.background = InfiniteBackground("assets/imgs/bg.png")
        self.ui = Ui(self.screen)

        # Entities
        self.player = Player(width // 2, height // 2, self.pointer)
        self.enemies = []
        self.entities = [self.player] + self.enemies

        # Screens
        self.game_over = GameOver(self.screen_width, self.screen_height)
        self.upgrade_menu = UpgradeMenu(self.player)

        self.spawn_timer = 0
        self.spawn_interval = 1.5  # seconds

        self.max_enemy = 10
        self.coins = []

        self.difficult_timer = 0
        self.difficult_interval = 60
        self.difficulty = 1

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state == "game_over":
                if self.game_over.handle_event(event):
                    self.__init__(
                        self.screen_width, self.screen_height, self.screen_title
                    )

            if self.game_state == "upgrade":
                self.upgrade_menu.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if self.game_state == "playing":
                        self.game_state = "upgrade"
                    elif self.game_state == "upgrade":
                        self.game_state = "playing"

    def spawn_enemy(self):
        spawn_distance = 400  # distance from player

        angle = random.uniform(0, 2 * 3.14159)
        direction = pygame.Vector2(math.cos(angle), math.sin(angle))

        spawn_pos = self.player.pos + direction * spawn_distance

        enemy = Enemy(self.player, spawn_pos.x, spawn_pos.y, self.difficulty)

        self.enemies.append(enemy)

    def attack_logic(self):
        if self.pointer.ranged:
            for projectile in self.player.projectiles:
                if not projectile.alive:
                    continue
                for enemy in self.enemies:
                    if not enemy.alive:
                        continue
                    to_enemy = enemy.pos - projectile.pos
                    if to_enemy.length() < projectile.radius + enemy.hurt_radius:
                        if enemy.hit(self.player):
                            self.coins.append(Coin(enemy.pos))
                        projectile.alive = False
        else:
            attack = self.player.attack
            if attack.active and attack.has_hit:
                for enemy in self.enemies:
                    if enemy in attack.hit_targets or not enemy.alive:
                        continue
                    to_enemy = enemy.pos - attack.hit_pos
                    if to_enemy.length() < attack.hit_radius:
                        if enemy.hit(self.player):
                            self.coins.append(Coin(enemy.pos))
                        attack.hit_targets.add(enemy)

    def update(self, dt):
        self.pointer.is_active = self.game_state == "playing"
        pygame.mouse.set_visible(self.game_state != "playing")

        if self.game_state == "game_over":
            self.game_over.update(dt)
            return

        if self.game_state == "upgrade":
            return

        if self.player.stats["hp"] <= 0:
            self.game_state = "game_over"

        self.timer += dt

        for entity in self.entities:
            entity.update(dt)

        self.camera.follow(self.player.rect)

        self.attack_logic()

        self.difficult_timer += dt
        if self.difficult_timer >= self.difficult_interval:
            self.difficult_timer = 0
            self.difficulty += 1
            self.max_enemy = 10 * self.difficulty
            self.spawn_interval = max(0.3, 1.5 / self.difficulty)

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            if len(self.enemies) < self.max_enemy:
                self.spawn_enemy()

        for coin in self.coins:
            coin.update(dt, self.player)

        self.coins = [c for c in self.coins if c.alive]

        self.enemies = [e for e in self.enemies if e.alive]
        self.entities = [self.player] + self.enemies

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen, self.camera.offset)

        self.entities.sort(key=lambda e: e.rect.bottom)

        for coin in self.coins:
            coin.draw(self.screen, self.camera)

        for entity in self.entities:
            entity.draw(self.screen, self.camera)

        self.ui.draw(self.player, self.timer)

        self.pointer.draw(self.screen, self.camera)

        if self.game_state == "upgrade":
            self.upgrade_menu.draw(self.screen)

        if self.game_state == "game_over":
            self.game_over.draw(self.screen)

    def start(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            dt = min(dt, 0.05)

            self.event_listener()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
