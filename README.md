# Gemini Engine

Gemini Engine is a monospace 2D ASCII rendering engine. It includes collisions, layers, inputs and the ability to handle solid objects as well as ascii art. The main library is currently contained in the gemini folder, and everything outside is examples.

WARNING: It’s important to use a monospace font in the terminal for the engine to render images properly

## Quick start

To get started, instance a Scene and an Entity, then render the scene

```python
from gemini import Scene, Entity

scene = Scene(size=(20,10))
entity = Entity(pos=(5,5),size=(2,1),parent=scene)

scene.render()
```

You should get something like this in your console:
```
░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░
░░░░░██░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░
```
Look at that! You just made your first Gemini project! Now try adding a while loop to the end of your code
```python
from gemini import sleep

while True:
	entity.move((1,0))
	scene.render()
	sleep(.1)
```

Now the entity should be moving across the screen! When the entity goes out of the screen's bounds it will loop back round to the other side.

## Sprites

the code below will animate a car moving across the screen:
```python
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