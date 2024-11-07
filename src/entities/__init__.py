"""
Пакет игровых сущностей.
Содержит все игровые объекты: игрок, враги, блоки и т.д.
"""

from .player import Player
from .enemy import Enemy
from .block import Block
from .coin import Coin
from .powerup import PowerUp

__all__ = [
    'Player',
    'Enemy',
    'Block',
    'Coin',
    'PowerUp'
]