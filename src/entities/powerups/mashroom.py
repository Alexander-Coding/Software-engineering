import pygame


class Mashroom(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game, variant):
        super().__init__(x, y, player, game)
        self.variant = variant