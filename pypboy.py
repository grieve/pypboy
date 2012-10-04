import pygame
import game.globals as globals
import game.core
import game.entities
import game.effects
import game.data
import game.radio

class Pypboy(game.core.Engine):

	def __init__(self, *args, **kwargs):
		super(Pypboy, self).__init__(*args, **kwargs)
		pygame.time.set_timer(self.EVENTS_UPDATE, 10)  # 100 updates per second
		pygame.time.set_timer(self.EVENTS_RENDER, 16)  # ~60 frames per second

		#Overlay
		overlay = game.entities.Overlay()
		self.add(overlay, "overlay")

		#Scanlines
		scanlines = game.effects.Scanlines(800, 480, 3, 1, [(0, 13, 3, 50), (6, 42, 22, 100), (0, 13, 3, 50)])
		self.add(scanlines, "scan")
		scanlines2 = game.effects.Scanlines(800, 480, 8, 4, [(0, 10, 1, 0), (21, 62, 42, 90), (61, 122, 82, 100), (21, 62, 42, 90)] + [(0, 10, 1, 0) for x in range(50)])
		self.add(scanlines2, "scan2")

		self.load_data()


	def run(self):
		self.running = True
		while self.running:
			for event in pygame.event.get():
				if (event.type == pygame.KEYDOWN):

					#Main Menu
					if (event.key == pygame.K_1):
						self.load_stats()
					if (event.key == pygame.K_2):
						self.load_items()
					if (event.key == pygame.K_3):
						self.load_data()

					#Submenu
					#How do we navigate the submenus?
					if (event.key == pygame.K_r):
						self.load_data(sub="Radio")
					if (event.key == pygame.K_s):
						try:
							self.get("radio").stop()
						except:
							pass
					if (event.key == pygame.K_p):
						try:
							self.get("radio").play()
						except:
							pass

					#Other Keys
					if (event.key == pygame.K_UP):
						try:
							self.get("mapper").move_map(0, -10)
						except:
							pass
					if (event.key == pygame.K_DOWN):
						try:
							self.get("mapper").move_map(0, 10)
						except:
							pass
					if (event.key == pygame.K_LEFT):
						try:
							self.get("mapper").move_map(-10, 0)
						except:
							pass
					if (event.key == pygame.K_RIGHT):
						try:
							self.get("mapper").move_map(10, 0)
						except:
							pass
					if (event.key == pygame.K_ESCAPE):
						self.running = False
				elif event.type == pygame.QUIT:
					self.running = False
				elif event.type == self.EVENTS_UPDATE:
					self.update()
				elif event.type == self.EVENTS_RENDER:
					self.render()

			pygame.time.wait(30)

		#turn off mixer
		try:
			pygame.mixer.quit()
		except:
			pass


	def load_stats(self, sub="Status"):

		self.rem("mapper")
		self.rem("radio")

		health = game.entities.Health()
		self.add(health, "health")

		#Header & Footer
		header = game.entities.Header("STATS", "The Gasworks")
		self.add(header, "header")
		footer = game.entities.Footer(globals.stat_menu, sub)
		self.add(footer, "footer")
		return self


	def load_items(self, sub="Weapons"):

		self.rem("mapper")
		self.rem("health")
		self.rem("radio")

		#Header & Footer
		header = game.entities.Header("ITEMS", "The Gasworks")
		self.add(header, "header")
		footer = game.entities.Footer(globals.item_menu, sub)
		self.add(footer, "footer")
		return self


	def load_data(self, sub="Local Map"):

		self.rem("mapper")
		self.rem("health")
		self.rem("radio")

		#Header & Footer
		header = game.entities.Header("DATA", "The Gasworks")
		self.add(header, "header")
		footer = game.entities.Footer(globals.data_menu, sub)
		self.add(footer, "footer")

		if sub == "Local Map":
			#Mapper
			# mapper = game.entities.Map(1200, pygame.Rect(0, 0, globals.WIDTH-8, globals.HEIGHT-80))
			# mapper.fetch_map((-77.02016830444336, 38.90319040137062), 0.01)
			# mapper.move_map(400, 560)
			# self.add(mapper,"mapper")
			mapgrid = game.entities.MapGrid((-5.936, 54.593), (globals.WIDTH - 8, globals.HEIGHT - 80))
			mapgrid.position = (4, 40)
			self.add(mapgrid, "mapgrid")

		elif sub == "Radio":
			#Radio
			radio = game.radio.Radio()
			self.add(radio, "radio")

		return self

