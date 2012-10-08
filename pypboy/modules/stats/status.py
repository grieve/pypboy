import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

	label = "Status"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		health = Health()
		self.add(health)


class Health(game.Entity):

	def __init__(self):
		self.image = pygame.image.load('images/pipboy.png')
		super(Health, self).__init__((config.WIDTH, config.HEIGHT))
		self.blit(self.image, (0, 0))
