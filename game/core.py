import pygame


class Engine(object):

	_children = []
	_layers = []
	EVENTS_UPDATE = pygame.USEREVENT + 1
	EVENTS_RENDER = pygame.USEREVENT + 2

	def __init__(self, title, width, height, *args, **kwargs):
		super(Engine, self).__init__(*args, **kwargs)
		self.window = pygame.display.set_mode((width, height))
		self.screen = pygame.display.get_surface()
		self.screen.fill((0, 23, 3))
		pygame.display.set_caption(title)
		pygame.font.init()

	def render(self):
		self.screen.fill((0, 0, 0))
		if hasattr(self, 'graphic'):
			self.screen.blit(self.graphic, (0, 0))

		for layer in self._layers:
			for child in layer:
				child.render()
				self.screen.blit(child, child.position)
		pygame.display.flip()

	def update(self):
		for child in self._children:
			child.update()

	# def rem(self, child):
	# 	try:
	# 		del self._children[child]
	# 		print "%s: removed %s" % (self, child)
	# 	except:
	# 		pass

	# def get(self, child):
	# 	return self._children[child]

	def add(self, child, layer=0):
		if isinstance(child, pygame.Surface):
			if len(self._layers) <= layer:
				for i in range((layer + 1) - len(self._layers)):
					self._layers.append([])
			self._children.append(child)
			self._layers[layer].append(child)
			print "%s: added %s" % (self, child)
		else:
			raise Exception("Child must be pygame.Surface")


class Entity(pygame.Surface):

	def __init__(self, size, *args, **kwargs):
		self._children = []
		self.position = (0, 0)
		super(Entity, self).__init__(size, flags=pygame.SRCALPHA, *args, **kwargs)

	def render(self, *args, **kwargs):
		if hasattr(self, 'graphic'):
			self.blit(self.graphic, (0, 0))
		for child in self._children:
			child.render()
			self.blit(child, child.position)

	def update(self, *args, **kwargs):
		for child in self._children:
			child.update()

	def add(self, child):
		if isinstance(child, pygame.Surface):
			self._children.append(child)
			print "%s: added %s" % (self, child)
		else:
			raise Exception("Child must be pygame.Surface")
