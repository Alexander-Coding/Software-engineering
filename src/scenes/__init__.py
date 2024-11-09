"""
Пакет сцен игры.
Содержит все игровые сцены: меню, уровни, настройки и т.д.
"""

from .menu import MainMenu
from .level import Level
from .level_select import LevelSelect
from .settings import Settings
from .controls_menu import ControlsMenu
from .game_over_menu import GameOverMenu
from .level_editor import LevelEditor

__all__ = [
    'MainMenu',
    'Level',
    'LevelSelect',
    'Settings',
    'LevelEditor',
    'ControlsMenu',
    'GameOverMenu'
]