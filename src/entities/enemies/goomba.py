import pygame
from resource_path import resource_path
from src.entities.enemy import Enemy


class Goomba(Enemy):
    def __init__(self, x, y, player, game, blocks, variant='dark'):
        super().__init__(x, y, player, game, blocks, variant)

        # Уникальные параметры для Goomba
        self.velocity_x = 2

        # Загружаем спрайты при инициализации
        self.load_sprites()

    @classmethod
    def get_variants(cls):
        return [
            {
                'enemy_name': 'goomba_dark',
                'image_path': 'assets/images/enemies/goombas/goomba_dark/walk1.png',
                'color': 'dark',
                'behavior': None
            }
        ]

    def load_sprites(self):
        sprite_paths = {
            'dark': {
                'idle': [
                    'assets/images/enemies/goombas/goomba_dark/walk1.png',
                    'assets/images/enemies/goombas/goomba_dark/walk2.png'
                ],
                'death': [
                    'assets/images/enemies/goombas/goomba_dark/squashed.png'
                ]
            }
        }
        self.sprites = {
            'idle': [
                pygame.image.load(resource_path(path)).convert_alpha()
                for path in sprite_paths[self.variant]['idle']
            ],
            'death': [
                pygame.image.load(resource_path(path)).convert_alpha()
                for path in sprite_paths[self.variant]['death']
            ]
        }
        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        if self.is_alive:
            self.move()
            self.take_damage()
            self.attack()
            super().update()

    def move(self):
        # Двигаем врага в зависимости от направления и скорости

        for block in self.blocks:
            # Проверка столкновения по оси X
            if block.rect.colliderect(self.rect.move(self.velocity_x, 0)):
                self.velocity_x = 0
                self.current_time = pygame.time.get_ticks()
                if self.current_time - self.last_reverse_time >= self.reverse_interval:
                    self.reverse_direction()
                    self.last_reverse_time = self.current_time
                    self.velocity_x = 2

            # Проверка столкновения по оси Y
            if block.rect.colliderect(self.rect.move(0, self.velocity_y)):
                if self.velocity_y > 0:  # Падение
                    self.rect.bottom = block.rect.top  # Устанавливаем игрока на верх блока
                    self.velocity_y = 0
                    self.on_ground = True  # Игрок на земле
                elif self.velocity_y < 0:  # Подъем (прыжок)
                    self.rect.top = block.rect.bottom  # Устанавливаем игрока на низ блока
                    self.velocity_y = 0
        if not self.handle_collision():
            self.on_ground = False

        self.rect.x += self.velocity_x * self.direction
        self.rect.y += self.velocity_y

    def attack(self):
        if self.is_alive:
            if self.current - self.attack_time >= self.reverse_interval:
                if self.rect.colliderect(self.player.rect.move(1, 0)) or self.rect.colliderect(self.player.rect.move(-1, 0)):
                    self.player.Death()

    def take_damage(self):
        self.current = pygame.time.get_ticks()
    # if not self.player.is_invincible():
        if self.rect.colliderect(self.player.rect.move(0, 1)):
            self.current_animation = "death"
            self.player.kill_enemy()
            self.die()

    def handle_collision(self):
        for block in self.blocks:
            if block.rect.colliderect(self.rect.move(0, 1)):  # Проверяем, есть ли коллизия с блоком чуть ниже персонажа
                return True
        return False