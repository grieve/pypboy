import pypboy
import pypboy.data
import pygame
import threading
import game


class Module(pypboy.SubModule):

	label = "Local Map"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		mapgrid = MapGrid((-5.936, 54.593), (game.globals.WIDTH - 8, game.globals.HEIGHT - 80))
		mapgrid.position = (4, 0)
		self.add(mapgrid)


class MapSquare(game.Entity):
	_mapper = None
	_size = 0
	_fetching = None
	_map_surface = None
	map_position = (0, 0)

	def __init__(self, size, map_position, *args, **kwargs):
		self._mapper = pypboy.data.Maps()
		self._size = size
		self._map_surface = pygame.Surface((size * 2, size * 2))
		self.map_position = map_position
		super(MapSquare, self).__init__((size, size), *args, **kwargs)

	def fetch_map(self):
		self._fetching = threading.Thread(target=self._internal_fetch_map)
		self._fetching.start()

	def _internal_fetch_map(self):
		self._mapper.fetch_grid(self.map_position)
		self.redraw_map()

	def update(self, *args, **kwargs):
		super(MapSquare, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		self.fill((0, 0, 0))
		self.blit(self._map_surface, (0, 0))
		super(MapSquare, self).render(*args, **kwargs)

	def redraw_map(self, coef=1):
		self._map_surface.fill((0, 0, 0))
		for way in self._mapper.transpose_ways((self._size, self._size), (self._size / 2, self._size / 2)):
			pygame.draw.lines(
					self._map_surface,
					(85, 251, 167),
					False,
					way,
					1
			)
		# for tag in self._mapper.transpose_tags((self._size, self._size), (self._size /2, self._size/2)):
		# 	try:
		# 		basicFont = pygame.font.SysFont(None, 18)
		# 		text = basicFont.render("%s" % tag[0], True, (95, 255, 177), (0, 0, 0))
		# 		text_width = text.get_size()[0]
		# 		pygame.draw.rect(
		# 			self._map_surface,
		# 			(0, 0, 0),
		# 			(tag[1] -5,tag[2]-5,text_width+10,25),
		# 			0
		# 		)
		# 		self._map_surface.blit(text, (tag[1], tag[2]))
		# 		pygame.draw.rect(
		# 			self._map_surface,
		# 			(95, 255, 177),
		# 			(tag[1] -5,tag[2]-5,text_width+10,25),
		# 			1
		# 		)
		# 	except Exception, e:
		# 		print(e)
		# 		pass


class MapGrid(game.Entity):

	_grid = None
	_delta = 0.002
	_starting_position = (0, 0)

	def __init__(self, starting_position, dimensions, *args, **kwargs):
		self._grid = []
		self._starting_position = starting_position
		super(MapGrid, self).__init__(dimensions, *args, **kwargs)
		self.test_fetch()

	def test_fetch(self):
		for x in range(10):
			for y in range(5):
				square = MapSquare(
					50,
					(
						self._starting_position[0] + (self._delta * x),
						self._starting_position[1] - (self._delta * y)
					)
				)
				square.fetch_map()
				square.position = (50 * x, 50 * y)
				self._grid.append(square)

	def render(self, *args, **kwargs):
		self.fill((0, 0, 0))
		for square in self._grid:
			self.blit(square._map_surface, square.position)
		super(MapGrid, self).render(*args, **kwargs)
