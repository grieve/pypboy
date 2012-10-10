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
		super(Health, self).__init__()
		self.image = pygame.image.load('images/pipboy.png')
		self.rect = self.image.get_rect()