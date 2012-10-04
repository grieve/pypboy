import pygame
import game
import game.globals
import os

class BaseModule(game.Entity):

	submodules = []

	def __init__(self, *args, **kwargs):
		super(BaseModule, self).__init__((game.globals.WIDTH, game.globals.HEIGHT))
		self.load_submodules()

	def parse_module(self, path):
		parts = path.split('.')
		module = parts[0]
		imp = __import__(module)
		for p in parts[1:]:
			if hasattr(imp, p):
				imp = getattr(imp, p)
			else:
				raise Exception('Module does not exist: %s' % path)
		return imp

	def load_submodules(self):
		for path, dirs, files in os.walk(os.path.dirname(__file__)):
			for f in files:
				if f.endswith(".py") and f != "__init__.py":
					path = "%s.%s" % (
						os.path.relpath(path).replace("/", "."),
						f[:-3]
					)
					module = self.parse_module(path)
					print module
					self.submodules.append(
						()
					)
					exit()


class SubModule(game.Entity):

	def __init__(self, *args, **kwargs):
		super(SubModule, self).__init__((globals.WIDTH - 8, globals.HEIGHT - 80))