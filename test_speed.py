from gemini import Scene, Entity
import random
from datetime import datetime

DISTANCE = 3
positions = [(0,6),(1,7),(3,9),(3,2),(1,5),(2,1),(6,2),(7,0),(3,2),(4,8),(2,6),(0,9),(1,0),(7,4),(4,9),(1,2),(3,4),(4,1),(4,8),(1,5)]

scene = Scene((10,10), is_main_scene=True)
scene.use_seperator = False
for pos in positions:
	new_entity = Entity(pos, (1,1))


before = datetime.now()
scene.render()
print(f"It took {datetime.now()-before} to render that")

before = datetime.now()
for child in scene.children:
	child.move(DISTANCE,0, collide=True)
print(f"It took {datetime.now()-before} to move that with collisions on")
before = datetime.now()
for child in scene.children:
	child.move(DISTANCE,0)
print(f"It took {datetime.now()-before} to move that with collisions off")


before = datetime.now()
scene.render()
print(f"It took {datetime.now()-before} to render that")