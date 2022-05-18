from gemini import Scene, Entity
import random
from datetime import datetime

scene = Scene((10,10), is_main_scene=True)
scene.use_seperator = False
for i in range(20):
	new_entity = Entity((random.randint(0,9), random.randint(0,9)), (1,1))


before = datetime.now()
scene.render()
print(f"It took {datetime.now()-before} to render that")

before = datetime.now()
for child in scene.children:
	child.move(2,0, collide=True)
print(f"It took {datetime.now()-before} to move that with collisions on")
before = datetime.now()
for child in scene.children:
	child.move(2,0)
print(f"It took {datetime.now()-before} to move that with collisions off")


before = datetime.now()
scene.render()
print(f"It took {datetime.now()-before} to render that")