import pypboy
import pypboy.data
import pygame
import threading
import game
import config


class Module(pypboy.SubModule):

	label = "Local Map"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		mapgrid = MapGrid((-5.9302032, 54.5966701), (config.WIDTH - 8, config.HEIGHT - 80))
		mapgrid.position = (4, 0)
		self.add(mapgrid)

	def handle_resume(self):
		self.parent.pypboy.header.headline = "DATA"
		self.parent.pypboy.header.title = "Farset's Mouth"
		super(Module, self).handle_resume()


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
		self.tags = {}
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
		self.blit(self._map_surface, (-self._size / 2, -self._size / 2))
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
		for tag in self._mapper.transpose_tags((self._size, self._size), (self._size / 2, self._size / 2)):
			self.tags[tag[0]] = (tag[1] + self.position[0], tag[2] + self.position[1], tag[3])


class MapGrid(game.Entity):

	_grid = None
	_delta = 0.002
	_starting_position = (0, 0)

	def __init__(self, starting_position, dimensions, *args, **kwargs):
		self._grid = []
		self._starting_position = starting_position
		self.dimensions = dimensions
		self._tag_surface = pygame.Surface(dimensions)
		super(MapGrid, self).__init__(dimensions, *args, **kwargs)
		self.tags = {}
		self.fetch_outwards()

	def test_fetch(self):
		for x in range(10):
			for y in range(5):
				square = MapSquare(
					100,
					(
						self._starting_position[0] + (self._delta * x),
						self._starting_position[1] - (self._delta * y)
					)
				)
				square.fetch_map()
				square.position = (100 * x, 100 * y)
				self._grid.append(square)

	def fetch_outwards(self):
		for x in range(-4, 4):
			for y in range(-2, 2):
				square = MapSquare(
					86,
					(
						self._starting_position[0] + (self._delta * x),
						self._starting_position[1] - (self._delta * y)
					)
				)
				square.fetch_map()
				square.position = ((86 * x) + (self.dimensions[0] / 2) - 43, (86 * y) + (self.dimensions[1] / 2) - 43)
				self._grid.append(square)


	def draw_tags(self):
		self.tags = {}
		for square in self._grid:
			self.tags.update(square.tags)
		self._tag_surface.fill((0, 0, 0))
		for name in self.tags:
			if self.tags[name][2] in config.AMENITIES:
				image = config.AMENITIES[self.tags[name][2]]
			else:
				print "Unknown amenity: %s" % self.tags[name][2]
				image = config.MAP_ICONS['misc']
			pygame.transform.scale(image, (10, 10))
			self.blit(image, (self.tags[name][0], self.tags[name][1]))
			# try:
			basicFont = pygame.font.SysFont(None, 12)
			text = basicFont.render(name, True, (95, 255, 177), (0, 0, 0))
			# text_width = text.get_size()[0]
			# 	pygame.draw.rect(
			# 		self,
			# 		(0, 0, 0),
			# 		(self.tags[name][0], self.tags[name][1], text_width + 4, 15),
			# 		0
			# 	)
			self.blit(text, (self.tags[name][0] + 17, self.tags[name][1] + 4))
			# 	pygame.draw.rect(
			# 		self,
			# 		(95, 255, 177),
			# 		(self.tags[name][0], self.tags[name][1], text_width + 4, 15),
			# 		1
			# 	)
			# except Exception, e:
			# 	print(e)
			# 	pass

	def render(self, *args, **kwargs):
		self.fill((0, 0, 0))
		for square in self._grid:
			self.blit(square._map_surface, square.position)
		self.draw_tags()
		super(MapGrid, self).render(*args, **kwargs)
