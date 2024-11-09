import pygame


class FireFlower(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game, variant='dark'):
        super().__init__()
        self.variant = variant