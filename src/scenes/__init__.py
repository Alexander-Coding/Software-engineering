"""
Пакет сцен игры.
Содержит все игровые сцены: меню, уровни, настройки и т.д.
"""

from .menu import MainMenu
from .level import Level
from .level_select import LevelSelect
from .settings import Settings
from .shop import Shop
from .level_editor import LevelEditor

__all__ = [
    'MainMenu',
    'Level',
    'LevelSelect',
    'Settings',
    'Shop',
    'LevelEditor'
]