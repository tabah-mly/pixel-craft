import pygame, random, math
from enemy import Enemy
from utils.camera import Camera
from utils.background import InfiniteBackground
from utils.pointer import Pointer
from utils.coin import Coin
from utils.game_over import GameOver
from utils.upgrade_menu import UpgradeMenu
from utils.ui import Ui


class GameBase:
    def initialize_screen_time(self):
        # Screens
        self.game_over = GameOver(self.screen_width, self.screen_height)
        self.upgrade_menu = UpgradeMenu(self.player)

        self.spawn_timer = 0
        self.spawn_interval = 1.5  # seconds

        self.max_enemy = 10
        self.coins = []

        self.timer = 0
        self.difficult_timer = 0
        self.difficult_interval = 30
        self.difficulty = 1

    def _spawn_enemy(self, player, difficulty, enemies):
        spawn_distance = 400  # distance from player

        angle = random.uniform(0, 2 * 3.14159)
        direction = pygame.Vector2(math.cos(angle), math.sin(angle))

        spawn_pos = player.pos + direction * spawn_distance

        enemy = Enemy(player, spawn_pos.x, spawn_pos.y, difficulty)

        enemies.append(enemy)

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

    def restart(self):
        self.__init__(self.screen_width, self.screen_height, self.screen_title)

    def draw_screen(self):
        if self.game_state == "upgrade":
            self.upgrade_menu.draw(self.screen)

        if self.game_state == "game_over":
            self.game_over.draw(self.screen)

    def update_screen(self, dt):
        self.pointer.is_active = self.game_state == "playing"
        pygame.mouse.set_visible(self.game_state != "playing")

        if self.game_state == "game_over":
            self.game_over.update(dt)
            return True

        if self.game_state == "upgrade":
            return True

    def screen_event_listener(self, event):
        if self.game_state == "game_over":
            if self.game_over.handle_event(event):
                self.restart()

        if self.game_state == "upgrade":
            self.upgrade_menu.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if self.game_state == "playing":
                    self.game_state = "upgrade"
                elif self.game_state == "upgrade":
                    self.game_state = "playing"

    def difficult_handler(self, dt):
        self.difficult_timer += dt
        if self.difficult_timer >= self.difficult_interval:
            self.difficult_timer = 0
            self.difficulty += 1
            self.max_enemy = 10 * self.difficulty
            self.spawn_interval = max(0.3, 1.5 / self.difficulty)

    def spawn_enemy(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            if len(self.enemies) < self.max_enemy:
                self._spawn_enemy(self.player, self.difficulty, self.enemies)

    def clean_entities(self):
        self.coins = [c for c in self.coins if c.alive]
        self.enemies = [e for e in self.enemies if e.alive]
        self.entities = [self.player] + self.enemies

    def check_game_over(self):
        if self.player.stats["hp"] <= 0:
            self.game_state = "game_over"

    def update_entities(self, dt):
        for entity in self.entities:
            entity.update(dt)

    def update_coin(self, dt):
        for coin in self.coins:
            coin.update(dt, self.player)

    def draw_coin(self):
        for coin in self.coins:
            coin.draw(self.screen, self.camera)

    def draw_entities(self):
        self.entities.sort(key=lambda e: e.rect.bottom)
        for entity in self.entities:
            entity.draw(self.screen, self.camera)

    def initialize_object(self):
        # UI
        self.pointer = Pointer()
        self.camera = Camera(self.screen_width, self.screen_height)
        self.background = InfiniteBackground("assets/imgs/bg.png")
        self.ui = Ui(self.screen)

    def set_fps(self, frame=60):
        dt = self.clock.tick(frame) / 1000
        return min(dt, 0.05)
