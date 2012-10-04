import game.globals
import pypboy
import modules

from modules.data import Module

if __name__ == "__main__":
	module = Module()
	boy = pypboy.Pypboy('Pip-Boy 3000', game.globals.WIDTH, game.globals.HEIGHT)
	boy.run()