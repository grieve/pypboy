import pypboy
import pygame
import game
import config
import pypboy.ui


class Module(pypboy.SubModule):

	label = "Status"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		health = Health()
		health.rect[0] = 4
		health.rect[1] = 40
		self.add(health)
		self.menu = pypboy.ui.Menu(100, ["CND", "RAD", "EFF"], [self.show_cnd, self.show_rad, self.show_eff], 0)
		self.menu.rect[0] = 4
		self.menu.rect[1] = 60
		self.add(self.menu)

	def handle_resume(self):
		self.parent.pypboy.header.headline = "STATUS"
		self.parent.pypboy.header.title = " HP 160/175  |  AP 62/62"
		super(Module, self).handle_resume()

	def show_cnd(self):
		print "CND"

	def show_rad(self):
		print "RAD"

	def show_eff(self):
		print "EFF"


class Health(game.Entity):

	def __init__(self):
		super(Health, self).__init__()
		self.image = pygame.image.load('images/pipboy.png')
		self.rect = self.image.get_rect()
		self.image = self.image.convert()
		text = config.FONTS[18].render("Grieve - Level 27", True, (105, 251, 187), (0, 0, 0))
		text_width = text.get_size()[0]
		self.image.blit(text, (config.WIDTH / 2 - 8 - text_width / 2, 250))
