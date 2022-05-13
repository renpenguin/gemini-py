# Gemini Engine

Gemini Engine is a monospace 2D ASCII rendering engine. It includes collisions, layers, inputs and the ability to handle solid objects as well as ascii art. The main library is currently contained in the gemini folder, and everything outside is examples.

## Quick start

the code below will animate a car moving across the screen:
```python3
from gemini import Scene, Sprite, sleep

car_image = """  ______
 /|_||_\`.__
(¶¶¶_¶¶¶¶_¶_\\
=`-(_)--(_)-'"""

scene = Scene((30,10), is_main_scene=True)
car = Sprite((5,5), car_image)

while True:
	scene.render()
	car.move(1,0)
	sleep(.1)
```