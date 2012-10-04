import pygame
import game

from modules import BaseModule

DISPLAY = 2
LABEL = "DATA"

class Module(BaseModule):

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)

		# #Header & Footer
		# header = game.entities.Header("DATA", "The Gasworks")
		# self.add(header, "header")
		# footer = game.entities.Footer(globals.data_menu, sub)
		# self.add(footer, "footer")

		# if sub == "Local Map":
		# 	#Mapper
		# 	# mapper = game.entities.Map(1200, pygame.Rect(0, 0, globals.WIDTH-8, globals.HEIGHT-80))
		# 	# mapper.fetch_map((-77.02016830444336, 38.90319040137062), 0.01)
		# 	# mapper.move_map(400, 560)
		# 	# self.add(mapper,"mapper")
		# 	mapgrid = game.entities.MapGrid((-5.936, 54.593), (globals.WIDTH - 8, globals.HEIGHT - 80))
		# 	mapgrid.position = (4, 40)
		# 	self.add(mapgrid, "mapgrid")

		# elif sub == "Radio":
		# 	#Radio
		# 	radio = game.radio.Radio()
		# 	self.add(radio, "radio")
