import pygame
pygame.mixer.init(44100, -16, 2, 2048)

import game.globals
from pypboy.core import Pypboy

if __name__ == "__main__":
	boy = Pypboy('Pip-Boy 3000', game.globals.WIDTH, game.globals.HEIGHT)
	boy.run()
