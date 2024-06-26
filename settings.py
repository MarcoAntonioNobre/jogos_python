# game setup
WIDTH = 1600
HEIGHT = 900
WIDTH_GAMEOVER = (WIDTH/100)*40
HEIGTH_GAMEOVER = (HEIGHT/100)*36

WIDTH_GAMEOVER2 = (WIDTH/100)*40-1
HEIGTH_GAMEOVER2 = (HEIGHT/100)*36-1
WIDTH_GAMEOVER_BUTTON = (WIDTH/100)*45
HEIGHT_GAMEOVER_BUTTON_RESTART = (HEIGHT/100)*50
HEIGHT_GAMEOVER_BUTTON_SAIR = (HEIGHT/100)*57
WIDTH_GAMEOVER_BUTTON_TELA_PAUSE = (WIDTH/100)*40-5
HEIGHT_GAMEOVER_BUTTON_SAIR_TELA_PAUSE = (HEIGHT/100)*92

FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0}

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 500
ENERGY_BAR_WIDTH = 440
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15, 'graphic': './graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30, 'graphic': './graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic': './graphics/weapons/axe/full.png'},
	'rapier': {'cooldown': 50, 'damage': 8, 'graphic': './graphics/weapons/rapier/full.png'},
	'sai': {'cooldown': 80, 'damage': 10, 'graphic': './graphics/weapons/sai/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'./graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'./graphics/particles/heal/heal.png'}}

# enemy
monster_data = {
	'squid': {'health': 140, 'exp': 110, 'damage': 25, 'attack_type': 'slash', 'attack_sound': './audio/attack/slash.wav', 'speed': 5, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 900, 'exp': 500, 'damage': 60, 'attack_type': 'claw',  'attack_sound': './audio/attack/claw.wav', 'speed': 6, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 130, 'exp': 150, 'damage': 10, 'attack_type': 'thunder', 'attack_sound': './audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 100, 'exp': 140, 'damage': 8, 'attack_type': 'leaf_attack', 'attack_sound': './audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}

