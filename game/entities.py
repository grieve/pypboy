import game
import game.data
import game.globals as globals
import pygame
import threading
import datetime

class Overlay(game.Entity):
	def __init__(self):
		self.image = pygame.image.load('images/overlay.png')
		super(Overlay, self).__init__((globals.WIDTH, globals.HEIGHT))
		self.blit_alpha(self, self.image, (0, 0), 128)
	
	def blit_alpha(self, target, source, location, opacity):
		x = location[0]
		y = location[1]
		temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		temp.blit(target, (-x, -y))
		temp.blit(source, (0, 0))
		temp.set_alpha(opacity)        
		target.blit(temp, location)

	def update(self, *args, **kwargs):
		super(Overlay, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		#self.blit_alpha(self, self.image, (0, 0), 128)
		super(Overlay, self).update(*args, **kwargs)
		

class Health(game.Entity):
	def __init__(self):
		self.image = pygame.image.load('images/pipboy.png')
		super(Health, self).__init__((globals.WIDTH, globals.HEIGHT))
		self.blit_alpha(self, self.image, (250, 85), 255)
	
	def blit_alpha(self, target, source, location, opacity):
		x = location[0]
		y = location[1]
		temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		temp.blit(target, (-x, -y))
		temp.blit(source, (0, 0))
		temp.set_alpha(opacity)        
		target.blit(temp, location)

	def update(self, *args, **kwargs):
		super(Health, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		#self.blit_alpha(self, self.image, (0, 0), 128)
		super(Health, self).update(*args, **kwargs)
		
		
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
		pygame.draw.line(self, (95, 255, 177), (10, 20), (10, 40), 2)
		pygame.draw.line(self, (95, 255, 177), (10, 20), (626, 20), 2)
		pygame.draw.line(self, (95, 255, 177), (626, 20), (626, 40), 2)
		pygame.draw.line(self, (95, 255, 177), (630, 20), (globals.WIDTH - 10, 20), 2)
		pygame.draw.line(self, (95, 255, 177), (globals.WIDTH - 10, 20), (globals.WIDTH - 10, 40), 2)

		basicFont = pygame.font.SysFont(None, 24)
		text = basicFont.render("   %s   " % self._headline, True, (105, 251, 187), (0, 0, 0))
		self.blit(text, (26, 15))
		text = basicFont.render(self._title, True, (95, 255, 177), (0, 0, 0))
		self.blit(text, (626 - text.get_width() - 10, 24))
		text = basicFont.render(self._date, True, (95, 255, 177), (0, 0, 0))
		self.blit(text, (656, 24))
		
		super(Header, self).update(*args, **kwargs)


class Footer(game.Entity):

	def __init__(self, menu, selected=None ):
		self.menu = menu
		if selected:
			self.selected = selected
		else:
			self.selected = menu[0]
		super(Footer, self).__init__((globals.WIDTH, globals.HEIGHT))

	def update(self, *args, **kwargs):
		super(Footer, self).update(*args, **kwargs)

	def render(self, *args, **kwargs):
		pygame.draw.line(self, (95, 255, 177), (10, globals.HEIGHT - 40), (10, globals.HEIGHT - 20), 2)
		pygame.draw.line(self, (95, 255, 177), (10, globals.HEIGHT - 20), (globals.WIDTH - 10, globals.HEIGHT - 20), 2)
		pygame.draw.line(self, (95, 255, 177), (globals.WIDTH - 10, globals.HEIGHT - 40), (globals.WIDTH - 10, globals.HEIGHT - 20), 2)
		
		offset = 50
		for m in self.menu:
			basicFont = pygame.font.SysFont(None, 24)
			text = basicFont.render("   %s   " % m, True, (105, 255, 187), (0, 0, 0))
			text_width = text.get_size()[0]
			#print(m+" : "+str(text.get_size()))
			if m == self.selected:
				pygame.draw.rect(self, (95, 255, 177), (offset-2, globals.HEIGHT - 36,(text_width+3), 26), 2)
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
				text = basicFont.render("%s" % tag[0], True, (95, 255, 177), (0, 0, 0))
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
				(95, 255, 177),
				(tag[1]-5,tag[2]-5,text_width+10,25),
				1
			    )
			except Exception, e:
				print(e)
				pass
