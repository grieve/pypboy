import game
import config
import pygame
import datetime


class Header(game.Entity):

	headline = "HEADER"
	title = "Title"
	_date = ""

	def __init__(self, headline, title):
		self.headline = headline
		self.title = title
		super(Header, self).__init__((config.WIDTH, config.HEIGHT))

	def update(self, *args, **kwargs):
		self._date = datetime.datetime.now().strftime("%d.%m.%y.%H:%M:%S")
		super(Header, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		pygame.draw.line(self, (95, 255, 177), (5, 15), (5, 35), 2)
		pygame.draw.line(self, (95, 255, 177), (5, 15), (config.WIDTH - 124, 15), 2)
		pygame.draw.line(self, (95, 255, 177), (config.WIDTH - 124, 15), (config.WIDTH - 124, 35), 2)
		pygame.draw.line(self, (95, 255, 177), (config.WIDTH - 120, 15), (config.WIDTH - 13, 15), 2)
		pygame.draw.line(self, (95, 255, 177), (config.WIDTH - 13, 15), (config.WIDTH - 13, 35), 2)

		basicFont = pygame.font.SysFont(None, 17)
		text = basicFont.render("   %s   " % self.headline, True, (105, 251, 187), (0, 0, 0))
		self.blit(text, (26, 8))
		text = basicFont.render(self.title, True, (95, 255, 177), (0, 0, 0))
		self.blit(text, ((config.WIDTH - 124) - text.get_width() - 10, 19))
		text = basicFont.render(self._date, True, (95, 255, 177), (0, 0, 0))
		self.blit(text, ((config.WIDTH - 111), 19))

		super(Header, self).update(*args, **kwargs)


class Footer(game.Entity):

	def __init__(self):
		self.menu = []
		super(Footer, self).__init__((config.WIDTH, config.HEIGHT))

	def update(self, *args, **kwargs):
		super(Footer, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		self.fill((0, 0, 0))
		pygame.draw.line(self, (95, 255, 177), (5, 2), (5, 20), 2)
		pygame.draw.line(self, (95, 255, 177), (5, 20), (config.WIDTH - 13, 20), 2)
		pygame.draw.line(self, (95, 255, 177), (config.WIDTH - 13, 2), (config.WIDTH - 13, 20), 2)

		offset = 50
		for m in self.menu:
			basicFont = pygame.font.SysFont(None, 16)
			text = basicFont.render("  %s  " % m, True, (105, 255, 187), (0, 0, 0))
			text_width = text.get_size()[0]
			#print(m+" : "+str(text.get_size()))
			if m == self.selected:
				pygame.draw.rect(self, (95, 255, 177), (offset - 2, 6, (text_width + 3), 26), 2)
			self.blit(text, (offset, 12))

			offset = offset + 120 + (text_width - 100)

		super(Footer, self).update(*args, **kwargs)


class Scanlines(game.Entity):

	def __init__(self, width, height, gap, speed, colours, *args, **kwargs):
		self.width = width
		self.height = height
		self.move = gap * len(colours)
		self.gap = gap
		self.colours = colours
		self.offset = 0
		self.speed = speed
		super(Scanlines, self).__init__((width, height), *args, **kwargs)

	def render(self, *args, **kwargs):
		colour = 0
		area = pygame.Rect(0, self.offset * self.speed, self.width, self.gap)
		while area.top <= self.height - self.gap:
			self.fill(self.colours[colour], area)
			area.move_ip(0, (self.gap))
			colour += 1
			if colour >= len(self.colours):
				colour = 0
		self.offset += 1
		if (self.offset * self.speed) >= self.move:
			self.offset = 0
		super(Scanlines, self).render(self, *args, **kwargs)


class Overlay(game.Entity):
	def __init__(self):
		self.image = pygame.image.load('images/overlay.png')
		super(Overlay, self).__init__((config.WIDTH, config.HEIGHT))
		self.blit_alpha(self, self.image, (0, 0), 128)

	def blit_alpha(self, target, source, location, opacity):
		x = location[0]
		y = location[1]
		temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		temp.blit(target, (-x, -y))
		temp.blit(source, (0, 0))
		temp.set_alpha(opacity)
		target.blit(temp, location)


class Border(game.Entity):
	def __init__(self):
		self.image = pygame.image.load('images/border.png')
		super(Border, self).__init__((config.WIDTH, config.HEIGHT))
		self.blit(self.image, (0, 0))
