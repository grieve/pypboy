import pygame
import config

try:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BOARD)
	config.GPIO_AVAILABLE = True
except Exception, e:
	print "GPIO UNAVAILABLE (%s)" % e
	config.GPIO_AVAILABLE = False

from pypboy.core import Pypboy

try:
	pygame.mixer.init(44100, -16, 2, 2048)
	config.SOUND_ENABLED = True
except:
	config.SOUND_ENABLED = False

if __name__ == "__main__":
	boy = Pypboy('Pip-Boy 3000', config.WIDTH, config.HEIGHT)
	boy.run()
