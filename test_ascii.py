from gemini import Scene, Sprite, AnimatedSprite, sleep, txtcolours as tc

scene1 = Scene((30,10))
bob = AnimatedSprite((10,3),["¯\_(ツ)_/¯","_/¯(ツ)¯\_"], parent=scene1, colour=tc.BOLD, extra_characters=[1])

test_image = """  ______
 /|_||_\`.__
(¶¶¶_¶¶¶¶_¶_\\
=`-(_)--(_)-'"""

scene2 = Scene((32,10), bg_colour=tc.CYAN)
scene2.use_seperator = False
car = Sprite((5,5), test_image, parent=scene2, colour=tc.GREEN)

while True:
	for direction in [(0,1),(-1,-1),(0,1),(1,-1)]:
		for _ in range(4):
			bob.move(direction[0],direction[1])
			car.move(1,0)
			scene1.render()
			scene2.render()
			sleep(.1)
		bob.next_frame()