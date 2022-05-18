from gemini import Scene, Sprite, Input, printd, sleep, txtcolours as tc

curses_input = Input()

wall_image = """
████████████████████████████████████████
█ █                                    █
█   █ █ ███████                        █
███   █ █                              █
█   ███                                █
█ ███   █                              █
█     ███                              █
█████ █                                █
█                     ██████████████████
█                     █                █
█                     █   And so, it   █
█                           begins
█                     █    the game    █
█                     █                █
████████████████████████████████████████
"""
scene = Scene((40, 15), is_main_scene=True, clear_char=" ")
walls = Sprite((0,-1),wall_image, colour=tc.BLUE)
player = Sprite((1,1),image="█", colour=tc.RED, auto_render=True, collisions=True)

scene.render()

while True:
	input = curses_input.get_key_press() # Wait for next key press, then move player, then render
	if input in ["w","a","s","d","up_arrow","down_arrow","left_arrow","right_arrow"]:
		match input:
			case "w"|"up_arrow":
				player.move(0,-1)
			case "a"|"left_arrow":
				player.move(-1,0)
			case "s"|"down_arrow":
				player.move(0,1)
			case "d"|"right_arrow":
				player.move(1,0)
	elif input in [" ","z"]:
		pass # Interact?