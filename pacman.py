from gemini import Scene, Sprite, Input, txtcolours as tc, sleep, add_pos

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

ghost_spawn_point = (8,8)

scene = Scene((17,19),clear_char=".", is_main_scene=True)
walls = Sprite((0,-1),image=pacman_board, colour=tc.BLUE, layer=3)
pacman = Sprite((8,13), "O", colour=tc.YELLOW, collisions=[3])

scene.render()

last_direction = (0,0)
direction = (0,0)

def try_set_direction(new_direction):
	global last_direction
	last_direction = new_direction
	if not scene.is_entity_at(add_pos(pacman.pos, new_direction)):
		global direction
		direction = new_direction

while True:
	scene.render()
	print(direction)
	print(last_direction)
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


	if not scene.is_entity_at(add_pos(pacman.pos, last_direction)):
		direction = last_direction
	pacman.move(direction)
	sleep(0.1)