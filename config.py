import pygame

WIDTH = 480
HEIGHT = 272

ACTIONS = {
	pygame.K_F1: "module_stats",
	pygame.K_F2: "module_items",
	pygame.K_F3: "module_data",
	pygame.K_1:	"knob_1",
	pygame.K_2: "knob_2",
	pygame.K_3: "knob_3",
	pygame.K_4: "knob_4",
	pygame.K_5: "knob_5",
	pygame.K_UP: "dial_up",
	pygame.K_DOWN: "dial_down"
}


MAP_ICONS = {
	"camp": pygame.image.load('images/map_icons/camp.png'),
	"factory": pygame.image.load('images/map_icons/factory.png'),
	"metro": pygame.image.load('images/map_icons/metro.png'),
	"misc": pygame.image.load('images/map_icons/misc.png'),
	"monument": pygame.image.load('images/map_icons/monument.png'),
	"vault": pygame.image.load('images/map_icons/vault.png'),
}

AMENITIES = {
	'fast_food': MAP_ICONS['camp'],
	'drinking_water': MAP_ICONS['camp'],
	'cinema': MAP_ICONS['factory'],
	'restaurant': MAP_ICONS['monument'],
	'pub': MAP_ICONS['vault'],
	'nightclub': MAP_ICONS['vault'],
	'cafe': MAP_ICONS['monument']
}
