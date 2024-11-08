"""
Пакет сущностей противников.
Содержит все игровые объекты противников
"""

import sys
import inspect

from .blooper import Blooper
from .beetle import Beetle
from .goomba import Goomba
from .koopa import Koopa


__all__ = [
    'Blooper',
    'Beetle',
    'Goomba',
    'Koopa'
]

def get_all_enemies():
    enemies = []
    current_module = sys.modules[__name__]

    for class_name in __all__:
        cls = getattr(current_module, class_name)
        
        if hasattr(cls, 'get_variants') and inspect.isclass(cls):
            variants = cls.get_variants()

            for variant in variants:
                enemies.append({
                    "class": class_name,
                    "enemy_name": variant["enemy_name"],
                    "image_path": variant["image_path"],
                    "color": variant["color"],
                    "behavior": variant["behavior"]
                })
    
    return enemies