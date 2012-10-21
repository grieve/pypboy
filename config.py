import pygame

WIDTH = 480
HEIGHT = 360

# OUTPUT_WIDTH = 480
# OUTPUT_HEIGHT = 360

MAP_FOCUS = (-5.9347681, 54.5889076)

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

# Using GPIO.BOARD as mode
GPIO_ACTIONS = {
	22: "module_stats",
	24: "module_items",
	26: "module_data",
	13:	"knob_1",
	11: "knob_2",
	7: "knob_3",
	5: "knob_4",
	3: "knob_5",
#	8: "dial_up",
#	7: "dial_down"
}


MAP_ICONS = {
	"camp": 		pygame.image.load('images/map_icons/camp.png'),
	"factory": 		pygame.image.load('images/map_icons/factory.png'),
	"metro": 		pygame.image.load('images/map_icons/metro.png'),
	"misc": 		pygame.image.load('images/map_icons/misc.png'),
	"monument": 	pygame.image.load('images/map_icons/monument.png'),
	"vault": 		pygame.image.load('images/map_icons/vault.png'),
	"settlement": 	pygame.image.load('images/map_icons/settlement.png'),
	"ruin": 		pygame.image.load('images/map_icons/ruin.png'),
	"cave": 		pygame.image.load('images/map_icons/cave.png'),
	"landmark": 	pygame.image.load('images/map_icons/landmark.png'),
	"city": 		pygame.image.load('images/map_icons/city.png'),
	"office": 		pygame.image.load('images/map_icons/office.png'),
	"sewer": 		pygame.image.load('images/map_icons/sewer.png'),
}

AMENITIES = {
	'pub': 				MAP_ICONS['vault'],
	'nightclub': 		MAP_ICONS['vault'],
	'bar': 				MAP_ICONS['vault'],
	'fast_food': 		MAP_ICONS['sewer'],
	'cafe': 			MAP_ICONS['sewer'],
	'drinking_water': 	MAP_ICONS['sewer'],
	'restaurant': 		MAP_ICONS['settlement'],
	'cinema': 			MAP_ICONS['office'],
	'pharmacy': 		MAP_ICONS['office'],
	'school': 			MAP_ICONS['office'],
	'bank': 			MAP_ICONS['monument'],
	'townhall': 		MAP_ICONS['monument'],
	'bicycle_parking': 	MAP_ICONS['misc'],
	'place_of_worship': MAP_ICONS['misc'],
	'theatre': 			MAP_ICONS['misc'],
	'bus_station': 		MAP_ICONS['misc'],
	'parking': 			MAP_ICONS['misc'],
	'fountain': 		MAP_ICONS['misc'],
	'marketplace': 		MAP_ICONS['misc'],
	'atm': 				MAP_ICONS['misc'],
}
