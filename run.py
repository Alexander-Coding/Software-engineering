import sys
import os

# Добавляем путь к исходникам в PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import Game

if __name__ == "__main__":
    game = Game()
    game.run()