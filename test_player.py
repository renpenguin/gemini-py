#!/usr/bin/env python3
from gemini import Scene, Entity, Sprite, Input, printd, sleep, txtcolours as tc

scene = Scene((40, 15), is_main_scene=True)
square = Entity((10,4),(2,1))
player = Sprite((20,7),image="ඞ", colour=tc.RED, auto_render=True, collisions=True)

scene.render()

while True:
	input = Input().get_key_press() # Wait for next key press, then move player, then render
	if input in ["w","a","s","d","up_arrow","down_arrow","left_arrow","right_arrow"]:
		match input:
			case "w"|"up_arrow":
				player.move(0,-1)
			case "a"|"left_arrow":
				player.move(-2,0)
			case "s"|"down_arrow":
				player.move(0,1)
			case "d"|"right_arrow":
				player.move(2,0)
	elif input in [" ","z"]:
		pass # Interact?