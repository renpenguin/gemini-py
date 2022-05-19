from gemini import Scene, Sprite, Input, txtcolours as tc, sleep

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
pacman = Sprite((8,13), "O", colour=tc.YELLOW, collisions=[3], auto_render=True)

scene.render()

last_direction = (0,0)
direction = (0,0)

def try_set_direction(direction):
	pass

while True:
	input = Input().pressed_key # Wait for next key press, then move player, then render
	if input in ["w","a","s","d","up_arrow","down_arrow","left_arrow","right_arrow"]:
		match input:
			case "w"|"up_arrow":
				last_direction = (0,-1)
			case "a"|"left_arrow":
				last_direction = (-1,0)
			case "s"|"down_arrow":
				last_direction = (0,1)
			case "d"|"right_arrow":
				last_direction = (1,0)

	if pacman.move(direction) == 1:
		direction = last_direction
		last_direction = (0,0)
	sleep(0.1)