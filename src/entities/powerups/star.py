import pygame


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game, variant='dark'):
        super().__init__()
        self.x = x
        self.y = y
        self.player = player
        self.game = game
        self.variant = variant
        self.load_sprites()

        # Анимация появления
        self.emerging = True
        self.emerge_height = 32
        self.initial_y = y
        self.movement_direction = 1  # 1 - вправо, -1 - влево
        self.speed = 2
        self.GRAVITY = 10
        self.velocity_y = 0
        self.tick = pygame.time.Clock().tick(60)


    @classmethod
    def get_variants(cls):
        return [
            {
                'item_name': 'star_dark',
                'image_path': 'assets/images/items/powerups/star_dark.png',
                'color': 'dark'
            },
            {
                'item_name': 'star_green',
                'image_path': 'assets/images/items/powerups/star_green.png',
                'color': 'green'
            },
            {
                'item_name': 'star_red',
                'image_path': 'assets/images/items/powerups/star_red.png',
                'color': 'red'
            },
            {
                'item_name': 'star_white',
                'image_path': 'assets/images/items/powerups/star_white.png',
                'color': 'white'
            }
        ]
    

    def load_sprites(self):       
        self.sprites = {
            'dark': [
                pygame.transform.scale(pygame.image.load('assets/images/items/powerups/star_dark.png'), (28, 28))
            ],
            'green': [
                pygame.transform.scale(pygame.image.load('assets/images/items/powerups/star_green.png'), (28, 28))
            ],
            'red': [
                pygame.transform.scale(pygame.image.load('assets/images/items/powerups/star_red.png'), (28, 28))
            ],
            'white': [
                pygame.transform.scale(pygame.image.load('assets/images/items/powerups/star_white.png'), (28, 28))
            ]
        }

        self.image = self.sprites[self.variant][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    
    def update(self):
        if self.emerging:
             self.emerge()


    def emerge(self):
        if self.rect.y > self.initial_y - self.emerge_height:
            self.rect.y -= 1
        else:
            self.emerging = False

    def update(self):
        if self.emerging:
            self.emerge()
        else:
            self.move()
            self.check_player_collision()

    def emerge(self):
        if self.rect.y > self.initial_y - self.emerge_height:
            self.rect.y -= 1
        else:
            self.emerging = False
            self.on_ground = True  # Разрешаем грибу теперь начать двигаться
            self.velocity_y = 0  # Сбрасываем вертикальную скорость при появлении

    def move(self):
        # Применяем гравитацию, если под грибом нет блоков
        if not self.check_block_below():
            self.velocity_y += self.GRAVITY * (self.tick / 1000)  # Применяем гравитацию к вертикальной скорости

            if self.velocity_y > 1:
                self.velocity_y = 1

            self.rect.y += self.velocity_y  # Обновляем позицию гриба по оси Y
        else:
            if not self.on_ground:  # Устанавливаем on_ground только при первом приземлении
                self.on_ground = True
                self.velocity_y = 0  # Сбрасываем вертикальную скорость

        # Перемещение гриба в зависимости от направления
        self.rect.x += self.movement_direction * self.speed

        # Проверка, есть ли блок перед грибом, меняем направление
        if self.on_ground and self.check_block_ahead():
            self.movement_direction *= -1  # Меняем направление, если перед грибом есть блок

    def check_block_below(self):
        # Проверка наличия блока под грибом
        for block in self.game.current_scene.blocks:
            if block.rect.colliderect(self.rect.move(0, 1)):  # Проверяем, есть ли коллизия с блоком чуть ниже гриба
                return True
            
        return False

    def check_block_ahead(self):
        # Проверка наличия блока перед грибом
        for block in self.game.current_scene.blocks:
            if block.rect.colliderect(self.rect.move(self.movement_direction * self.speed, 0)):  # Проверяем, есть ли коллизия с блоком впереди
                return True
            
        return False

    def check_player_collision(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.player.get_invulnerability()
            self.game.game_state.score += 100
            self.game.sound_manager.play_sound('powerup')
            self.kill()
