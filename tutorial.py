from gemini import printd, Input, Scene, Entity, sleep

def example():
	"""Run this to explore Gemini Engine
	>>> import gemini
	>>> gemini.example()"""

	printd("Gemini Engine is a monospaced 2D ASCII-based rendering engine. Press space to see an example, and press ^C after that to continue the demo")
	while True:
		if Input().pressed_key == " ":
			break

	scene = Scene((30,10))
	square = Entity((0,5),(1,1), parent=scene)
	i = -1
	while True:
		scene.render()
		square.move(1 if i%60<30 else -1, 0)
		try:
			sleep(.1)
		except KeyboardInterrupt:
			break
		i += 1
	printd("This is the piece of code that allowed the little square to go back and forth on the scene\n> from gemini import Entity, Scene, sleep\n> scene = Scene(width=30,height=10)\n> square = Entity(pos=(0,5),size=(2,1), parent=scene)\n> i = -1\n> while True:\n>   scene.render()\n>   square.move(1 if i%60<30 else -1, 0)\n>   sleep(.1)\n>   i += 1")
	printd("Simple, right? Gemini uses a style similar to how old film projectors used to work, by printing a completely new image in the same place where the previous one was. If you scroll up, you'll be able to see all the frames you rendered!")
	printd("Now get creative! It's time to see what you can make")

if __name__ == "__main__":
	example()