import game
import game.data
import game.globals as globals
import pygame
import threading
import datetime

class Header(game.Entity):

	_headline = "HEADER"
	_title = "Title"
	_date = ""

	def __init__(self, headline, title):
		self._headline = headline
		self._title = title
		super(Header, self).__init__((globals.WIDTH, globals.HEIGHT))

	def update(self, *args, **kwargs):
		self._date = datetime.datetime.now().strftime("%d.%m.%y.%H:%M:%S")
		super(Header, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		pygame.draw.line(self, (85, 251, 167), (4, 14), (4, 36), 2)
		pygame.draw.line(self, (85, 251, 167), (4, 14), (626, 14), 2)
		pygame.draw.line(self, (85, 251, 167), (626, 14), (626, 36), 2)
		pygame.draw.line(self, (85, 251, 167), (630, 14), (globals.WIDTH - 6, 14), 2)
		pygame.draw.line(self, (85, 251, 167), (globals.WIDTH - 6, 14), (globals.WIDTH - 6, 36), 2)

		basicFont = pygame.font.SysFont(None, 24)
		text = basicFont.render("   %s   " % self._headline, True, (85, 251, 167), (0, 0, 0))
		self.blit(text, (16, 5))
		text = basicFont.render(self._title, True, (85, 251, 167), (0, 0, 0))
		self.blit(text, (626 - text.get_width() - 10, 18))
		text = basicFont.render(self._date, True, (85, 251, 167), (0, 0, 0))
		self.blit(text, (656, 18))
		super(Header, self).update(*args, **kwargs)


class Footer(game.Entity):

	def __init__(self, menu):
		self.menu = menu
		self.selected = menu[0]
		super(Footer, self).__init__((globals.WIDTH, globals.HEIGHT))

	def update(self, *args, **kwargs):
		super(Footer, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		pygame.draw.line(self, (85, 251, 167), (4, globals.HEIGHT - 40), (4, globals.HEIGHT - 20), 2)
		pygame.draw.line(self, (85, 251, 167), (4, globals.HEIGHT - 20), (globals.WIDTH - 6, globals.HEIGHT - 20), 2)
		pygame.draw.line(self, (85, 251, 167), (globals.WIDTH - 6, globals.HEIGHT - 40), (globals.WIDTH - 6, globals.HEIGHT - 20), 2)
		
		offset = 50
		for m in self.menu:
			basicFont = pygame.font.SysFont(None, 24)
			text = basicFont.render("   %s   " % m, True, (85, 251, 167), (0, 0, 0))
			text_width = text.get_size()[0]
			#print(m+" : "+str(text.get_size()))
			if m == self.selected:
				pygame.draw.rect(self, (85, 251, 167), (offset-2, globals.HEIGHT - 36,(text_width+3), 26), 2)
			self.blit(text, (offset, 450))
			
			offset = offset + 160 + (text_width - 100)
		
		super(Footer, self).update(*args, **kwargs)


class Map(game.Entity):

	_mapper = None
	_transposed = None
	_size = 0
	_fetching = None
	_map_surface = None
	_loading_size = 0
	_render_rect = None

	def __init__(self, width, render_rect=None, *args, **kwargs):
		self._mapper = game.data.Maps()
		self._size = width
		self._map_surface = pygame.Surface((width, width))
		self._render_rect = render_rect
		super(Map, self).__init__((width, width), *args, **kwargs)
		self.position = (4, 45)

	def fetch_map(self, position, radius):
		#(-5.9234923, 54.5899493)
		self._fetching = threading.Thread(target=self._internal_fetch_map, args=(position, radius))
		self._fetching.start()

	def _internal_fetch_map(self, position, radius):
		self._mapper.fetch_grid(position)
		self.redraw_map()

	def update(self, *args, **kwargs):
		super(Map, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		self.fill((0, 0, 0))
		# if self._fetching.is_alive():
		# 	pygame.draw.circle(self, (255, 255, 255), (11, 11), self._loading_size)
		# 	self._loading_size += 1
		# 	if self._loading_size >= 10:
		# 		self._loading_size = 0
		# else:
		self.blit(self._map_surface, (0, 0), area=self._render_rect)
		super(Map, self).render(*args, **kwargs)

	def move_map(self, x, y):
		self._render_rect.move_ip(x, y)

	def redraw_map(self, coef=1):
		self._map_surface.fill((0, 0, 0))
		for way in self._mapper.transpose_ways((self._size/coef, self._size/coef), (self._size / 2, self._size / 2)):
			pygame.draw.lines(
				self._map_surface,
				(85, 251, 167),
				False,
				way,
				2
			)
		for tag in self._mapper.transpose_tags((self._size/coef, self._size/coef), (self._size / 2, self._size / 2)):
			try:
				basicFont = pygame.font.SysFont(None, 18)
				text = basicFont.render("%s" % tag[0], True, (145, 255, 227), (0, 0, 0))
				text_width = text.get_size()[0]
				pygame.draw.rect(
				self._map_surface,
				(0, 0, 0),
				(tag[1]-5,tag[2]-5,text_width+10,25),
				0
			    )
				self._map_surface.blit(text, (tag[1],tag[2]))
				pygame.draw.rect(
				self._map_surface,
				(85, 251, 167),
				(tag[1]-5,tag[2]-5,text_width+10,25),
				1
			    )
			except Exception, e:
				print(e)
				pass
