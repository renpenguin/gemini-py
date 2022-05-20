from gemini import Scene, Entity, sleep, add_pos, txtcolours as tc, Input
import math

colours = tc.ALL_COLOURS

scene = Scene((30,15), is_main_scene=True)

brick = Entity((14,7), (2,1))

i = 0
while True:
	sleep(.01)
	if Input().pressed_key == " ":
		break
	i += 0.05*math.pi
	# new_brick = Entity(brick.pos, (2,1), colour=colours[int(i%len(colours))])
	brick.pos = add_pos((14,7), (round(10*math.cos(i)), round(5*math.sin(i))))
	scene.render()