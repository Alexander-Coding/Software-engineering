import pygame
from src.config import *
from resource_path import resource_path


class FinalCreditsScene:
    def __init__(self, game):
        self.game = game
        self.credits = [
            "Разработчики:", 
            "Кодеры и по совместительству профессиональные дебаггеры:",
            "",
            "1. Главный из главных – Руководитель команды / Скрам-мастер:",
            "Гоняет нас по спринтам как ветром по степи.",
            "Тот, кто следит за дедлайнами и иногда даже пишет код:",
            "Колупаев Александр",
            "",
            "2. Разработчик 1:",
            "Король коммитов и мастер Ctrl+C и Ctrl+V.",
            "Никогда не сдаётся в битве с багами, если не найдет нового.",
            "Сопов Никита",
            "",
            "3. Разработчик 2:",
            "Скрытый гений оптимизации: превращает 1000 строк кода в одну, но зато какую!",
            "Любит кофе и вечный цикл if (sleep_needed) { coffee++; }",
            "Лысенко Никита",
            "",
            "4. Разработчик 3:",
            "Легенда git merge и повелитель undo.",
            "Тот, кто постоянно говорит: «А у меня всё работает!»",
            "Колупаев Александр",
            "",
            "5. Разработчик 4:",
            "Бесстрашный борец с исключениями, которые никто не мог победить.",
            "Живёт по принципу: «Багов нет, есть скрытые фичи»",
            "Ерофеев Тимур",
            "",
            "Музыка:",
            "Эпические треки из нашей единой на всех библиотеки с бесплатной лицензией.",
            "Или когда компилятор выдаёт ошибку – это уже своя мелодия…",
            "",
            "Особая благодарность преподавателю: За вдохновение, советы и веру, что мы справимся", 
            "(ну, или почти справимся).",
            "",
            "Спасибо за просмотр!",
            "Мы потратили на этот проект достаточно ночей, чтобы заслужить нечто большее, чем просто усталость.",
            "Поэтому просим зачет! Или хотя бы пересдачу, если вы дочитали до конца и улыбнулись :)"
        ]
        self.font = pygame.font.Font(None, 36)  # Шрифт для отображения текста
        self.credit_y = WINDOW_HEIGHT  # Начальная позиция за пределами экрана
        self.scroll_speed = 1  # Скорость прокрутки титров

        self.game.sound_manager.play_music('titles')
        self.background_image = pygame.image.load(resource_path('assets/images/backgrounds/final_scene.png')).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def update(self):
        # Обновляем позицию титров, уменьшая значение по оси Y для плавного движения вверх
        self.credit_y -= self.scroll_speed
        # Сбрасываем позицию, когда все титры вышли за верхнюю границу экрана
        if self.credit_y < -len(self.credits) * 50:
            self.credit_y = WINDOW_HEIGHT

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.go_to_main_menu()

    def draw(self, screen):
        # Отрисовка фона
        screen.blit(self.background_image, (0, 0))

        # Отрисовка каждого элемента титров с медленным движением вверх
        for i, line in enumerate(self.credits):
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, self.credit_y + i * 50))
            screen.blit(text, text_rect)

    def go_to_main_menu(self):
        from src.scenes.menu import MainMenu
        self.game.change_scene(MainMenu(self.game))
