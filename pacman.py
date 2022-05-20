from gemini import Scene, Entity, Sprite, AnimatedSprite, Input, txtcolours as tc, sleep, add_pos

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

scene = Scene((17,19),clear_char=" ", is_main_scene=True)
walls = Sprite((0,-1),image=pacman_board, colour=tc.BLUE, layer=3)

total_pac_dots = 0

for x in range(scene.size[0]):
	for y in range(scene.size[1]):
		if not scene.is_entity_at((x,y)):
			total_pac_dots += 1
			pac_dot = Entity((x,y), (1,1), fill_char='.', layer=5)

pacman = AnimatedSprite((8,13), ['O', 'C'], colour=tc.YELLOW, collisions=[3], layer=1)
pacman.move_functions.append(pacman.next_frame)

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

	if not scene.is_entity_at(add_pos(pacman.pos, last_direction), pacman.collisions):
		direction = last_direction
	if pacman.move(direction) == 1:
		direction = (0,0)
	if scene.is_entity_at(pacman.pos, [5]):
		total_pac_dots -= 1
		removed_dot: Sprite = scene.get_entities_at(pacman.pos)[0]
		removed_dot.parent = None
		del removed_dot

		if len(scene.children) < 3:
			break

	sleep(0.1)

scene.render()
print("\nYou win!\n")