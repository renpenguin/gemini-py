from gemini import Scene, Entity, Sprite, txtcolours as tc, sleep

test_image = """  ______
 /|_||_\`.__
(¶¶¶_¶¶¶¶_¶_\\
=`-(_)--(_)-'"""

scene = Scene((30,10), bg_colour=tc.CYAN, is_main_scene=True)
car = Sprite((5,5), test_image, colour=tc.GREEN)

car.hide()
car.show()

while True:
	scene.render()
	car.move(1,0)
	sleep(.1)