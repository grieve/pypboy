import game
import game.data
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
		super(Header, self).__init__((800, 480))

	def update(self, *args, **kwargs):
		self._date = datetime.datetime.now().strftime("%d.%m.%y.%H:%M:%S")
		super(Header, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		pygame.draw.line(self, (85, 251, 167), (4, 14), (4, 36), 2)
		pygame.draw.line(self, (85, 251, 167), (4, 14), (626, 14), 2)
		pygame.draw.line(self, (85, 251, 167), (626, 14), (626, 36), 2)
		pygame.draw.line(self, (85, 251, 167), (630, 14), (794, 14), 2)
		pygame.draw.line(self, (85, 251, 167), (794, 14), (794, 36), 2)

		pygame.draw.line(self, (85, 251, 167), (4, 444), (4, 466), 2)
		pygame.draw.line(self, (85, 251, 167), (4, 444), (794, 444), 2)
		pygame.draw.line(self, (85, 251, 167), (794, 444), (794, 466), 2)

		basicFont = pygame.font.SysFont(None, 24)
		text = basicFont.render("   %s   " % self._headline, True, (85, 251, 167), (0, 0, 0))
		self.blit(text, (16, 5))
		text = basicFont.render(self._title, True, (85, 251, 167), (0, 0, 0))
		self.blit(text, (626 - text.get_width() - 10, 18))
		text = basicFont.render(self._date, True, (85, 251, 167), (0, 0, 0))
		self.blit(text, (656, 18))
		super(Header, self).update(*args, **kwargs)


class Footer(game.Entity):

	def __init__(self):
		super(Footer, self).__init__((800, 480))

	def update(self, *args, **kwargs):
		super(Footer, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
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
		self._mapper.fetch_by_coordinate(position, radius)
		self.redraw_map()

	def update(self, *args, **kwargs):
		super(Map, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		self.fill((0, 0, 0))
		if self._fetching.is_alive():
			pygame.draw.circle(self, (255, 255, 255), (11, 11), self._loading_size)
			self._loading_size += 1
			if self._loading_size >= 10:
				self._loading_size = 0
		else:
			self.blit(self._map_surface, (0, 0), area=self._render_rect)
		super(Map, self).render(*args, **kwargs)

	def move_map(self, x, y):
		self._render_rect.move_ip(x, y)

	def redraw_map(self):
		for way in self._mapper.transpose_ways((self._size, self._size), (self._size / 2, self._size / 2)):
			pygame.draw.lines(
				self._map_surface,
				(85, 251, 167),
				False,
				way,
				2
			)
