import game
import pygame
import threading
import datetime


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
		#	   pygame.draw.circle(self, (255, 255, 255), (11, 11), self._loading_size)
		#	   self._loading_size += 1
		#	   if self._loading_size >= 10:
		#			   self._loading_size = 0
		# else:
		self.blit(self._map_surface, (0, 0), area=self._render_rect)
		super(Map, self).render(*args, **kwargs)

	def move_map(self, x, y):
		self._render_rect.move_ip(x, y)

	def redraw_map(self, coef=1):
		self._map_surface.fill((0, 0, 0))
		for way in self._mapper.transpose_ways((self._size / coef, self._size / coef), (self._size / 2, self._size / 2)):
			pygame.draw.lines(
					self._map_surface,
					(85, 251, 167),
					False,
					way,
					2
			)
		for tag in self._mapper.transpose_tags((self._size / coef, self._size / coef), (self._size / 2, self._size / 2)):
			try:
				basicFont = pygame.font.SysFont(None, 18)
				text = basicFont.render("%s" % tag[0], True, (95, 255, 177), (0, 0, 0))
				text_width = text.get_size()[0]
				pygame.draw.rect(
				self._map_surface,
				(0, 0, 0),
				(tag[1] - 5, tag[2] - 5, text_width + 10, 25),
				0
			)
				self._map_surface.blit(text, (tag[1], tag[2]))
				pygame.draw.rect(
				self._map_surface,
				(95, 255, 177),
				(tag[1] - 5, tag[2] - 5, text_width + 10, 25),
				1
			)
			except Exception, e:
				print(e)
				pass
