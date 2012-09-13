import pygame
import game.core
import game.entities
import game.effects

if __name__ == "__main__":
	engine = game.core.Engine('Pip-Boy 3000', 800, 480)

	header = game.entities.Header("DATA", "The Gasworks")
	engine.add(header)

	mapper = game.entities.Map(1600, pygame.Rect(0, 0, 792, 390))
	#mapper.fetch_map((-5.9234923, 54.5899493), 0.02)
	mapper.fetch_map((-73.9654541015625, 40.78184126814031), 0.02)
	mapper.move_map(400, 560)
	engine.add(mapper)

	scanlines = game.effects.Scanlines(800, 480, 10, [(21, 62, 42, 100), (0, 23, 3, 100)])
	engine.add(scanlines)

	while True:
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
		engine.update()
		engine.render()
