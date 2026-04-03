import pygame
from utils.spritesheet import SpriteSheet


class Enemy:
    def __init__(self, player, x, y, difficulty):
        self.animations = {
            "walk": SpriteSheet("assets/imgs/enemy_walk.png", 4, 0.1),
            "hit": SpriteSheet("assets/imgs/enemy_hit.png", 4, 0.1),
            "attack": SpriteSheet("assets/imgs/enemy_attack.png", 4, 0.1),
        }

        self.state = "walk"
        self.facing_right = True
        self.animator = self.animations[self.state]
        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(center=(x, y))

        self.player = player

        self.stun_timer = 0
        self.stun_duration_min = 0.2  # Since our animation has 2 frame and each frame are 0.1s we'll use 0.2s for the minimum duration

        self.alive = True
        self.hurt_radius = 30

        self.stats = {
            "max_hp": 100 * 0.5 * difficulty,
            "hp": 100 * 0.5 * difficulty,
            "damage": 5 * 0.5 * difficulty,
            "speed": 100 * 0.5 * difficulty,
            "attack_range": 50 * 0.5 * difficulty,
        }

        self.is_attack = False

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def move(self, dt):
        direction = self.player.pos - self.pos
        distance = direction.length()

        if distance > self.stats["attack_range"]:
            direction = direction.normalize()

            self.pos += direction * self.stats["speed"] * dt
            self.rect.center = self.pos
            self.set_state("walk")
            self.is_attack = False
        else:
            if self.state != "attack":
                self.set_state("attack")
                self.animator.reset()
                self.is_attack = False

            self.attack()

    def attack(self):
        # Hit on frame 4
        if self.animator.frame_index == 4 and not self.is_attack:
            self.player.stats["hp"] -= self.stats["damage"]
            self.player.stats["hp"] = int(max(self.player.stats["hp"], 0))
            self.is_attack = True

        if self.animator.frame_index == 0:
            self.is_attack = False

    def update(self, dt):
        if not self.alive:
            return

        self.animator.update(dt)

        if self.stun_timer > 0:  # Count down stun, and skip the movement
            self.stun_timer -= dt
            return

        self.move(dt)

    def draw(self, surface, camera):
        if not self.alive:
            return

        image = self.animator.image.copy()

        if not self.stun_timer > 0:
            self.facing_right = self.player.pos.x >= self.pos.x

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        surface.blit(image, camera.apply(self.rect))

    def hit(self, player):
        self.stun_timer = max(
            self.stun_duration_min, player.stats["stun"]
        )  # Start stun
        self.set_state("hit")

        self.pos += player.pointer.direction * player.stats["knockback"]
        self.rect.center = self.pos
        self.stats["hp"] -= player.stats["damage"]

        if self.stats["hp"] <= 0:
            self.alive = False
            player.items["killed"] += 1
            return True

        return False
