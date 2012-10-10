import pygame
import config

from pypboy.core import Pypboy

try:
	pygame.mixer.init(44100, -16, 2, 2048)
	config.SOUND_ENABLED = True
except:
	config.SOUND_ENABLED = False

if __name__ == "__main__":
	boy = Pypboy('Pip-Boy 3000', config.WIDTH, config.HEIGHT)
	boy.run()
