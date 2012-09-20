import pygame
import game.globals as globals
import game.core
import game.entities
import game.effects
import game.data

if __name__ == "__main__":
	engine = game.core.Engine('Pip-Boy 3000', globals.WIDTH, globals.HEIGHT)

	header = game.entities.Header("DATA", "The Gasworks")
	engine.add(header)
	
	

	mapper = game.entities.Map(1200, pygame.Rect(0, 0, globals.WIDTH-8, globals.HEIGHT-80))
	#mapper.fetch_map((-5.9234923, 54.5899493), 0.02)
	mapper.fetch_map((-77.02016830444336, 38.90319040137062), 0.01)
	mapper.move_map(400, 560)
	engine.add(mapper)
	
	footer = game.entities.Footer(game.data.menus)
	engine.add(footer)

	scanlines = game.effects.Scanlines(800, 480, 3, 1, [(11, 52, 32, 100), (0, 23, 3, 100)])
	scanlines2 = game.effects.Scanlines(800, 480, 8, 3, [(0, 23, 3, 100),(21, 62, 42, 100),(61, 102, 82, 100),(21, 62, 42, 100)] + [(0, 23, 3, 100) for x in range(50)])
	engine.add(scanlines)
	engine.add(scanlines2)
	running = True

	while running:
		
		for event in pygame.event.get():
			if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_UP):
					mapper.move_map(0, -5)
				if (event.key == pygame.K_DOWN):
					mapper.move_map(0, 5)
				if (event.key == pygame.K_LEFT):
					mapper.move_map(-5, 0)
				if (event.key == pygame.K_RIGHT):
					mapper.move_map(5, 0)
				if (event.key == pygame.K_ESCAPE):
					running = False
			elif event.type == pygame.QUIT:
				running = False
					
		engine.update()
		engine.render()
		pygame.time.wait(30)
