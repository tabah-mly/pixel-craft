class Camera:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0

    def follow(self, target):
        # Center on player
        self.x = target.rect.centerx - (self.game.screen_width // 2)
        self.y = target.rect.centery - (self.game.screen_height // 2)
