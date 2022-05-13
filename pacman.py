from gemini import Scene, Sprite, Input, txtcolours as tc

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
║ ═╗ ══   ══ ╔═ ║
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
pacman = Sprite((8,12), "O", colour=tc.YELLOW, collisions=[3])

scene.render()

while True:
	input = Input().get_key_press() # Wait for next key press, then move player, then render
	if input in ["w","a","s","d","up_arrow","down_arrow","left_arrow","right_arrow"]:
		match input:
			case "w"|"up_arrow":
				pacman.move(0,-1)
			case "a"|"left_arrow":
				pacman.move(-1,0)
			case "s"|"down_arrow":
				pacman.move(0,1)
			case "d"|"right_arrow":
				pacman.move(1,0)
		scene.render()