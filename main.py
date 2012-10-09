import pygame
pygame.mixer.init(44100, -16, 2, 2048)
from pypboy.core import Pypboy
import config

if __name__ == "__main__":
	boy = Pypboy('Pip-Boy 3000', config.WIDTH, config.HEIGHT)
	boy.run()
