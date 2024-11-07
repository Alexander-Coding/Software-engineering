"""
Пакет утилит.
Содержит вспомогательные модули: загрузчик ресурсов, физика, система очков и т.д.
"""

from .asset_loader import AssetLoader
from .save_system import SaveSystem
from .physics import PhysicsEngine
from .scoring import ScoringSystem
from .animation import Animation, AnimationController
from .sound_manager import SoundManager

__all__ = [
    'AssetLoader',
    'SaveSystem',
    'PhysicsEngine',
    'ScoringSystem',
    'Animation',
    'AnimationController',
    'SoundManager'
]