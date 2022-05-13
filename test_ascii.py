from gemini import Scene, Sprite, sleep, txtcolours as tc

scene = Scene((30,10))
scene.use_seperator = False
bob = Sprite((5,3),"¯\_(ツ)_/¯", parent=scene, auto_render=True, colour=tc.BOLD, extra_characters=[1])

while True:
	for direction in [(1,0),(0,1),(-1,0),(0,-1)]:
		for _ in range(4):
			bob.move(direction[0],direction[1])
			sleep(.1)