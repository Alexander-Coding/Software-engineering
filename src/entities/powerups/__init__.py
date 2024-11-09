"""
Пакет игровых предметов.
Содержит игровые предметы: монета, гриб, звезда, цветок
"""

import sys
import inspect

from .fireflower import FireFlower
from .mashroom import Mashroom
from .star import Star


__all__ = [
    'FireFlower',
    'Mashroom',
    'Star'
]


def get_all_powerups():
    powerups = []
    current_module = sys.modules[__name__]

    for class_name in __all__:
        cls = getattr(current_module, class_name)
        
        if hasattr(cls, 'get_variants') and inspect.isclass(cls):
            variants = cls.get_variants()

            for variant in variants:
                powerups.append({
                    "class": class_name,
                    "item_name": variant["item_name"],
                    "image_path": variant["image_path"],
                    "color": variant["color"]
                })
    
    return powerups


