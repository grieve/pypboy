import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

	label = "Status"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		health = Health()
		health.rect[0] = 4
		health.rect[1] = 40
		self.add(health)

	def handle_resume(self):
		self.parent.pypboy.header.headline = "STATUS"
		self.parent.pypboy.header.title = "Grieve - Level 27"
		super(Module, self).handle_resume()


class Health(game.Entity):

	def __init__(self):
		super(Health, self).__init__()
		self.image = pygame.image.load('images/pipboy.png')
		self.rect = self.image.get_rect()
