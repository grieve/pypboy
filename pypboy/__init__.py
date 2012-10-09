import pygame
import game
import config
import pypboy.ui


class BaseModule(game.Entity):

	submodules = []

	def __init__(self, boy, *args, **kwargs):
		super(BaseModule, self).__init__((config.WIDTH, config.HEIGHT - 40))
		self.pypboy = boy
		self.position = (0, 40)

		self.footer = pypboy.ui.Footer()
		self.footer.menu = []
		for mod in self.submodules:
			self.footer.menu.append(mod.label)
		self.footer.selected = self.footer.menu[0]
		self.footer.position = (0, config.HEIGHT - 80)
		self.add(self.footer)

		self.init_submodules()

		self.action_handlers = {
			"pause": self.handle_pause,
			"resume": self.handle_resume
		}

		self.module_change_sfx = pygame.mixer.Sound('sounds/module_change.ogg')

	def init_submodules(self):
		self.module_surface = game.core.Entity((config.WIDTH - 8, config.HEIGHT - 80))
		self.add(self.module_surface)
		self.switch_submodule(0)

	def switch_submodule(self, module):
		if hasattr(self, 'active') and self.active:
			self.active.handle_action("pause")
		if len(self.submodules) > module:
			self.active = self.submodules[module]
			self.active.parent = self
			self.active.handle_action("resume")
			self.footer.selected = self.footer.menu[module]
		else:
			print "No submodule at %d" % module

	def render(self):
		self.active.render()
		self.module_surface.fill((0, 0, 0))
		self.module_surface.blit(self.active, (0, 0))
		super(BaseModule, self).render()

	def handle_action(self, action, value=0):
		if action.startswith("knob_"):
			num = int(action[-1])
			self.switch_submodule(num - 1)
		elif action in self.action_handlers:
			self.action_handlers[action]()
		else:
			if hasattr(self, 'active') and self.active:
				self.active.handle_action(action, value)

	def handle_pause(self):
		self.paused = True

	def handle_resume(self):
		self.paused = False
		self.module_change_sfx.play()


class SubModule(game.Entity):

	def __init__(self, parent, *args, **kwargs):
		super(SubModule, self).__init__((config.WIDTH - 8, config.HEIGHT - 80))
		self.parent = parent

		self.action_handlers = {
			"pause": self.handle_pause,
			"resume": self.handle_resume
		}

		self.submodule_change_sfx = pygame.mixer.Sound('sounds/submodule_change.ogg')
		self.dial_move_sfx = pygame.mixer.Sound('sounds/dial_move.ogg')

	def handle_action(self, action, value=0):
		if action.startswith("dial_"):
			self.dial_move_sfx.play()
			if action[4:] == "up":
				pass
			else:
				pass
		elif action in self.action_handlers:
			self.action_handlers[action]()

	def handle_pause(self):
		self.paused = True

	def handle_resume(self):
		self.paused = False
		self.submodule_change_sfx.play()
