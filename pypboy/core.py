import pygame
import config
import game
import pypboy.ui

from pypboy.modules import data
from pypboy.modules import items
from pypboy.modules import stats


class Pypboy(game.core.Engine):

	def __init__(self, *args, **kwargs):
		super(Pypboy, self).__init__(*args, **kwargs)

		self.init_children()
		self.init_modules()

	def init_children(self):
		overlay = pypboy.ui.Overlay()
		self.add(overlay, 100)
		border = pypboy.ui.Border()
		self.add(border, 9999)
		self.header = pypboy.ui.Header("DATA", "The Gasworks")
		self.add(self.header, 10)
		scanlines = pypboy.ui.Scanlines(800, 480, 3, 1, [(0, 13, 3, 50), (6, 42, 22, 100), (0, 13, 3, 50)])
		self.add(scanlines, 999)
		scanlines2 = pypboy.ui.Scanlines(800, 480, 8, 4, [(0, 10, 1, 0), (21, 62, 42, 90), (61, 122, 82, 100), (21, 62, 42, 90)] + [(0, 10, 1, 0) for x in range(50)])
		self.add(scanlines2, 999)

	def init_modules(self):
		self.modules = {
			"data": data.Module(),
			"items": items.Module(),
			"stats": stats.Module()
		}
		self.active = self.modules["data"]
		self.module_surface = game.core.Entity((config.WIDTH - 8, config.HEIGHT - 40))
		self.module_surface.position = (4, 40)
		self.add(self.module_surface, 10)

	def update(self):
		self.active.update()
		super(Pypboy, self).update()

	def render(self):
		self.active.render()
		self.module_surface.blit(self.active, (0, 0))
		super(Pypboy, self).render()

	def switch_module(self, module):
		if module in self.modules:
			self.active.handle_action("pause")
			self.active = self.modules[module]
			self.active.handle_action("resume")
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