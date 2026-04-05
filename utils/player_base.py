import pygame
from utils.projectile import Projectile
from utils.attack import Attack


class PlayerBase:
    def initialize(self, x, y, pointer):
        self.state = "idle"
        self.facing_right = True
        self.animator = self.animations[self.state]
        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(center=(x, y))

        self.pointer = pointer

        self.is_attack = False
        self.attack_timer = 0
        self.attack_duration = 0.15

        self.prev_mouse_left = False
        self.prev_mouse_right = False

        self.hurt_radius = 30

        self.projectiles = []
        self.attack = Attack()

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def mouse_handler(self):
        mouse = pygame.mouse.get_pressed()

        # Change attack type (ranged or melee)
        if mouse[2] and not self.prev_mouse_right:
            self.pointer.ranged = not self.pointer.ranged
        self.prev_mouse_right = mouse[2]

        # Acttack Logic
        if mouse[0] and not self.prev_mouse_left:
            if self.pointer.ranged:
                if self.pointer.direction.length_squared() > 0:
                    projectile = Projectile(
                        self.pos, self.pointer.direction, self.stats["speed"]
                    )
                    self.projectiles.append(projectile)
            else:
                self.attack.start()

        self.projectiles = [p for p in self.projectiles if p.alive]
        self.prev_mouse_left = mouse[0]

    def move(self, direction, dt):
        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.pos += direction * self.stats["speed"] * dt
            self.rect.center = self.pos
            self.set_state("walk")
        else:
            self.set_state("idle")

    def update_projectiles(self, dt):
        for projectile in self.projectiles:
            projectile.update(dt)

    def draw_attack(self, surface, camera):
        for projectile in self.projectiles:
            projectile.draw(surface, camera)

        self.attack.draw(surface, camera, self.pos)

    def draw_sprites(self, surface, camera):
        image = self.animator.image
        mouse_x = pygame.mouse.get_pos()[0]
        center_screen_x = surface.get_width() // 2

        if self.pointer.is_active:
            self.facing_right = mouse_x >= center_screen_x

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        player_rect = camera.apply(self.rect)
        surface.blit(image, player_rect)
