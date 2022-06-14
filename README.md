# Gemini Engine

[![PyPI version](https://img.shields.io/pypi/v/gemini-engine?logo=pypi)](https://pypi.org/project/gemini-engine) ![Stars](https://img.shields.io/github/stars/redpenguinyt/GeminiEngine?color=yellow) ![Last commit](https://img.shields.io/github/last-commit/redpenguinyt/geminiengine) ![Code size](https://img.shields.io/github/languages/code-size/redpenguinyt/GeminiEngine) [![Downloads](https://img.shields.io/pypi/dm/gemini-engine)](https://pypi.org/project/gemini-engine) [![Issues](https://img.shields.io/github/issues/redpenguinyt/geminiengine)](https://github.com/redpenguinyt/GeminiEngine/issues)

Gemini Engine is a monospace 2D ASCII rendering engine. It includes collisions, layers, inputs and the ability to handle solid objects as well as ascii art. Examples can be found on the [GeminiExamples github](https://github.com/redpenguinyt/GeminiExamples)

WARNING: It’s important to use a monospace font in the terminal for the engine to render images properly

## Quick start

Gemini Engine can be installed using pip:

```
python3 -m pip install -U gemini-engine
```

If you want to run the latest version of the code, you can install from github:

```
python3 -m pip install -U git+https://github.com/redpenguinyt/GeminiEngine.git@latest
```

Now that you have installed the library, instance a Scene and an Entity, then render the scene

```py
from gemini import Scene, Entity

scene = Scene(size=(20,10))
entity = Entity(pos=(5,5), size=(2,1), parent=scene)

scene.render()
```

You should get something like this in your console:
![Gemini example 1](https://i.imgur.com/57daGVq.png)

Look at that! You just made your first Gemini project! Now try adding a while loop to the end of your code
```py
from gemini import Scene, Entity, sleep

scene = Scene(size=(20,10))
entity = Entity(pos=(5,5), size=(2,1), parent=scene)

while True:
	entity.move((1,0))
	scene.render()
	sleep(.1)
```

Now the entity should be moving across the screen! When the entity goes out of the screen's bounds it will loop back round to the other side.

## Sprites

The code below will animate a car moving across the screen:
```py
from gemini import Scene, Sprite, sleep

car_image = """
  ______
 /|_||_\`.__
(¶¶¶_¶¶¶¶_¶_\\
=`-(_)--(_)-'
"""

scene = Scene((30,10), is_main_scene=True)
car = Sprite((5,5), car_image)

while True:
	scene.render()
	car.move(1,0)
	sleep(.1)
```