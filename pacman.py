from gemini import Scene, Entity, Sprite, AnimatedSprite, Input, txtcolours as tc, sleep, add_pos
import random

USE_POWERUPS = False

pacman_board = """
╔═══════╦═══════╗
║       ║       ║
║ ██ ██ ║ ██ ██ ║
║               ║
║ ══ ║ ═╦═ ║ ══ ║
║    ║  ║  ║    ║
╚══╗ ╠═ ║ ═╣ ╔══╝
═══╝ ║     ║ ╚═══
       ███
═══╗ ║     ║ ╔═══
╔══╝ ║ ═╦═ ║ ╚══╗
║       ║       ║
║ ═╗ ══ ║ ══ ╔═ ║
║  ║         ║  ║
╠═ ║ ║ ═╦═ ║ ║ ═╣
║    ║  ║  ║    ║
║ ═══╩═ ║ ═╩═══ ║
║               ║
╚═══════════════╝
"""

smell_board = [
	((0, 8), -136), ((1, 1), -315), ((1, 2), -317), ((1, 3), -303), ((1, 4), -304), ((1, 5), -305), ((1, 8), -135), ((1, 11), -125), ((1, 12), -124), ((1, 13), -121), ((1, 15), -116), ((1, 16), -115), ((1, 17), -114), ((2, 1), -314), ((2, 3), -302), ((2, 5), -306), ((2, 8), -134), ((2, 11), -127), ((2, 13), -120), ((2, 14), -119), ((2, 15), -118), ((2, 17), -113), ((3, 1), -313), ((3, 3), -301), ((3, 5), -307), ((3, 8), -133), ((3, 11), -128), ((3, 15), -223), ((3, 17), -112), ((4, 1), -292), ((4, 2), -291), ((4, 3), -290), ((4, 4), -309), ((4, 5), -308), ((4, 6), -325), ((4, 7), -326), ((4, 8), -132), ((4, 9), -131), ((4, 10), -130), ((4, 11), -79), ((4, 12), -78), ((4, 13), -77), ((4, 14), -227), ((4, 15), -224), ((4, 17), -111), ((5, 1), -293), ((5, 3), -289), ((5, 8), -141), ((5, 11), -80), ((5, 13), -76), ((5, 17), -110), ((6, 1), -294), ((6, 3), -186), ((6, 4), -189), ((6, 5), -190), ((6, 7), -143), ((6, 8), -142), ((6, 9), -239), ((6, 10), -238), ((6, 11), -81), ((6, 13), -55), ((6, 14), -58), ((6, 15), -59), ((6, 17), -109), ((7, 1), -295), ((7, 2), -296), ((7, 3), -185), ((7, 5), -191), ((7, 6), -194), ((7, 7), -149), ((7, 9), 0), ((7, 11), -82), ((7, 12), -85), ((7, 13), -54), ((7, 15), -60), ((7, 16), -61), ((7, 17), -62), ((8, 3), -184), ((8, 7), -150), ((8, 9), -1), ((8, 13), -53), ((8, 17), -63), ((9, 1), -283), ((9, 2), -284), ((9, 3), -183), ((9, 5), -178), ((9, 6), -177), ((9, 7), -151), ((9, 9), -2), ((9, 11), -6), ((9, 12), -42), ((9, 13), -41), ((9, 15), -66), ((9, 16), -65), ((9, 17), -64), ((10, 1), -282), ((10, 3), -182), ((10, 4), -181), ((10, 5), -179), ((10, 7), -152), ((10, 8), -13), ((10, 9), -3), ((10, 10), -4), ((10, 11), -5), ((10, 13), -40), ((10, 14), -70), ((10, 15), -69), ((10, 17), -105), ((11, 1), -281), ((11, 3), -256), ((11, 8), -14), ((11, 11), -46), ((11, 13), -39), ((11, 17), -104), ((12, 1), -266), ((12, 2), -265), ((12, 3), -257), ((12, 4), -277), ((12, 5), -18), ((12, 6), -17), ((12, 7), -16), ((12, 8), -15), ((12, 9), -22), ((12, 10), -23), ((12, 11), -24), ((12, 12), -48), ((12, 13), -37), ((12, 14), -36), ((12, 15), -35), ((12, 17), -103), ((13, 1), -267), ((13, 3), -258), ((13, 5), -275), ((13, 8), -202), ((13, 11), -25), ((13, 15), -34), ((13, 17), -102), ((14, 1), -268), ((14, 3), -259), ((14, 5), -274), ((14, 8), -203), ((14, 11), -26), ((14, 13), -30), ((14, 14), -32), ((14, 15), -33), ((14, 17), -101), ((15, 1), -269), ((15, 2), -270), ((15, 3), -260), ((15, 4), -272), ((15, 5), -273), ((15, 8), -204), ((15, 11), -27), ((15, 12), -28), ((15, 13), -29), ((15, 15), -97), ((15, 16), -98), ((15, 17), -99), ((16, 8), -205)
]

def try_set_direction(new_direction):
	global last_direction
	last_direction = new_direction
	if not scene.is_entity_at(add_pos(pacman.pos, new_direction)):
		global direction
		direction = new_direction

# Setup

scene = Scene((17,19),clear_char=" ",is_main_scene=True)
walls = Sprite((0,-1),image=pacman_board, colour=tc.BLUE, layer=3)
pacman = AnimatedSprite((8,13), ['O','ᗤ','Ↄ','ᗤ'], colour=tc.YELLOW, collisions=[3], layer=1)
pacman.move_functions.append(pacman.next_frame)
last_direction = (0,0)
direction = (0,0)

# Dots

total_pac_dots = 0
for x in range(scene.size[0]):
	for y in range(scene.size[1]):
		if not scene.is_entity_at((x,y), layers=[3]):
			total_pac_dots += 1
			pac_dot = Entity((x,y), (1,1), layer=5)
			pac_dot.powerup = (x,y) in [(1,1),(15,1),(1,17),(15,17)] and USE_POWERUPS
			pac_dot.fill_char = "•" if pac_dot.powerup else "."

def collect_dots():
	for smell in smell_points:
		smell.smell -= 1

	if scene.is_entity_at(pacman.pos, 5):
		global total_pac_dots
		total_pac_dots -= 1
		removed_dot = scene.get_entities_at(pacman.pos, [5])[0]
		if removed_dot.powerup:
			global ghosts_scared
			ghosts_scared = 50
		removed_dot.parent = None
		del removed_dot

		if len(list(filter(lambda x: x.layer == 5, scene.children))) == 0:
			return 1

# Pathfinding

def get_smell_at(pos):
	result = scene.get_entities_at(pos, 10)
	if len(result) > 0:
		return result[0]

smell_points = []

for pos, smell in smell_board:
	pac_smell = Sprite(pos, ' ', layer=10)
	smell_points.append(pac_smell)
	pac_smell.smell = smell

# Ghosts

ghost_colours = [tc.RED, tc.YELLOW, tc.CYAN, tc.GREEN]
ghosts = [
	Sprite((8,7), 'ᗣ', colour=colour, layer=4, collisions=[3]) for colour in ghost_colours
]
for i, g in enumerate(ghosts): g.wait_time = (i+1)*20
ghosts_scared = 0

def move_ghosts():
	global gametime, ghosts_scared
	if ghosts_scared > 0:
		ghosts_scared -= 1
	for i, ghost in enumerate(ghosts):
		if ghost.wait_time > 0:
			ghost.wait_time -= 1
			continue
		if ghosts_scared > 15:
			ghost.colour = tc.BLUE
		elif ghosts_scared > 0:
			ghost.colour = tc.BLUE if gametime % 6 > 2 else ""
		else:
			ghost.colour = ghost_colours[i]
		if random.randint(0,10) > 3:
			directions = [get_smell_at(add_pos(ghost.pos,dir,limits=scene.size)) for dir in [(1,0),(-1,0),(0,1),(0,-1)]]
			directions = list(filter(lambda x: x is not None, directions))
			direction = sorted(directions, key=lambda x: x.smell, reverse=ghosts_scared==0)[0]
			ghost.move((add_pos(direction.pos, ghost.pos, int.__sub__)))

gametime = 0
game_over = False
while not game_over:
	gametime += 1
	scene.render()
	print(f"Dots left: {total_pac_dots}")
	input = Input().pressed_key # Wait for next key press, then move player, then render
	if input in ["w","a","s","d","up_arrow","down_arrow","left_arrow","right_arrow"]:
		match input:
			case "w"|"up_arrow":
				try_set_direction((0,-1))
			case "a"|"left_arrow":
				try_set_direction((-1,0))
			case "s"|"down_arrow":
				try_set_direction((0,1))
			case "d"|"right_arrow":
				try_set_direction((1,0))
	elif input == " ":
		break

	get_smell_at(pacman.pos).smell = 0
	if collect_dots() == 1:
		scene.render()
		print("\nYou win!\n")
		game_over = True
	move_ghosts()

	if not scene.is_entity_at(add_pos(pacman.pos, last_direction), pacman.collisions):
		direction = last_direction
	if pacman.move(direction) == 1:
		direction = (0,0)

	for ghost in ghosts:
		if scene.is_entity_at(ghost.pos, pacman.layer):
			if ghosts_scared > 0:
				ghost.pos = (8,7)
				ghost.wait_time = 25
			else:
				scene.render()
				print("\nYou lose!\n")
				game_over = True

	sleep(0.1)