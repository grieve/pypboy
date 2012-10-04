import pygame
import game.globals as globals
import game.core
import game.entities
import game.effects
import game.data
import game.radio


def load_stats(engine, sub="Status"):

	engine.rem("mapper")
	engine.rem("radio")

	health = game.entities.Health()
	engine.add(health, "health")

	#Header & Footer
	header = game.entities.Header("STATS", "The Gasworks")
	engine.add(header, "header")
	footer = game.entities.Footer(globals.stat_menu, sub)
	engine.add(footer, "footer")
	return engine


def load_items(engine, sub="Weapons"):

	engine.rem("mapper")
	engine.rem("health")
	engine.rem("radio")

	#Header & Footer
	header = game.entities.Header("ITEMS", "The Gasworks")
	engine.add(header, "header")
	footer = game.entities.Footer(globals.item_menu, sub)
	engine.add(footer, "footer")
	return engine


def load_data(engine, sub="Local Map"):

	engine.rem("mapper")
	engine.rem("health")
	engine.rem("radio")

	#Header & Footer
	header = game.entities.Header("DATA", "The Gasworks")
	engine.add(header, "header")
	footer = game.entities.Footer(globals.data_menu, sub)
	engine.add(footer, "footer")

	if sub == "Local Map":
		#Mapper
		# mapper = game.entities.Map(1200, pygame.Rect(0, 0, globals.WIDTH-8, globals.HEIGHT-80))
		# mapper.fetch_map((-77.02016830444336, 38.90319040137062), 0.01)
		# mapper.move_map(400, 560)
		# engine.add(mapper,"mapper")
		mapgrid = game.entities.MapGrid((-5.936, 54.593), (globals.WIDTH - 8, globals.HEIGHT - 80))
		mapgrid.position = (4, 40)
		engine.add(mapgrid, "mapgrid")

	elif sub == "Radio":
		#Radio
		radio = game.radio.Radio()
		engine.add(radio, "radio")

	return engine


if __name__ == "__main__":
	engine = game.core.Engine('Pip-Boy 3000', globals.WIDTH, globals.HEIGHT)

	#Overlay
	overlay = game.entities.Overlay()
	engine.add(overlay, "overlay")

	#Scanlines
	scanlines = game.effects.Scanlines(800, 480, 3, 1, [(0, 13, 3, 50), (6, 42, 22, 100), (0, 13, 3, 50)])
	engine.add(scanlines, "scan")
	scanlines2 = game.effects.Scanlines(800, 480, 8, 4, [(0, 10, 1, 0), (21, 62, 42, 90), (61, 122, 82, 100), (21, 62, 42, 90)] + [(0, 10, 1, 0) for x in range(50)])
	engine.add(scanlines2, "scan2")

	engine = load_data(engine)

	running = True
	while running:
		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN):

				#Main Menu
				if (event.key == pygame.K_1):
					engine = load_stats(engine)
				if (event.key == pygame.K_2):
					engine = load_items(engine)
				if (event.key == pygame.K_3):
					engine = load_data(engine)

				#Submenu
				#How do we navigate the submenus?
				if (event.key == pygame.K_r):
					engine = load_data(engine, sub="Radio")
				if (event.key == pygame.K_s):
					try:
						engine.get("radio").stop()
					except:
						pass
				if (event.key == pygame.K_p):
					try:
						engine.get("radio").play()
					except:
						pass

				#Other Keys
				if (event.key == pygame.K_UP):
					try:
						engine.get("mapper").move_map(0, -10)
					except:
						pass
				if (event.key == pygame.K_DOWN):
					try:
						engine.get("mapper").move_map(0, 10)
					except:
						pass
				if (event.key == pygame.K_LEFT):
					try:
						engine.get("mapper").move_map(-10, 0)
					except:
						pass
				if (event.key == pygame.K_RIGHT):
					try:
						engine.get("mapper").move_map(10, 0)
					except:
						pass
				if (event.key == pygame.K_ESCAPE):
					running = False
			elif event.type == pygame.QUIT:
				running = False

		engine.update()
		engine.render()
		pygame.time.wait(30)

	#turn off mixer
	try:
		pygame.mixer.quit()
	except:
		pass
