import pygame
import config
import game
import pypboy.ui

#from pypboy.modules import data
#from pypboy.modules import items
from pypboy.modules import stats


class Pypboy(game.core.Engine):

	def __init__(self, *args, **kwargs):
		super(Pypboy, self).__init__(*args, **kwargs)
		self.init_children()
		self.init_modules()

	def init_children(self):
		self.background = pygame.image.load('images/overlay.png')
		# border = pypboy.ui.Border()
		# self.root_children.add(border)
		self.header = pypboy.ui.Header()
		self.root_children.add(self.header)
		scanlines = pypboy.ui.Scanlines(800, 480, 3, 1, [(0, 13, 3, 50), (6, 42, 22, 100), (0, 13, 3, 50)])
		self.root_children.add(scanlines)
		scanlines2 = pypboy.ui.Scanlines(800, 480, 8, 4, [(0, 10, 1, 0), (21, 62, 42, 90), (61, 122, 82, 100), (21, 62, 42, 90)] + [(0, 10, 1, 0) for x in range(50)])
		self.root_children.add(scanlines2)

	def init_modules(self):
		self.modules = {
			#"data": data.Module(self),
			#"items": items.Module(self),
			"stats": stats.Module(self)
		}
		for module in self.modules.values():
			module.move(4, 40)
		self.switch_module("stats")

	def update(self):
		if hasattr(self, 'active'):
			self.active.update()
		super(Pypboy, self).update()

	def render(self):
		if hasattr(self, 'active'):
			self.active.render()
		super(Pypboy, self).render()

	def switch_module(self, module):
		if module in self.modules:
			if hasattr(self, 'active'):
				self.active.handle_action("pause")
				self.remove(self.active)
			self.active = self.modules[module]
			self.active.parent = self
			self.active.handle_action("resume")
			self.add(self.active)
		else:
			print "Module '%s' not implemented." % module

	def run(self):
		self.running = True
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_ESCAPE):
						self.running = False
					else:
						if event.key in config.ACTIONS:
							action = config.ACTIONS[event.key]
							if action.startswith('module_'):
								self.switch_module(action[7:])
							else:
								if hasattr(self, 'active'):
									self.active.handle_action(config.ACTIONS[event.key])
				elif event.type == pygame.QUIT:
					self.running = False

			self.update()
			self.render()
			pygame.time.wait(10)

		try:
			pygame.mixer.quit()
		except:
			pass
