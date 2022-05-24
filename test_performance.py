from gemini import Scene, Entity
import random
from datetime import datetime

DISTANCE = 2
positions = [(0,6),(1,7),(3,9),(3,2),(1,5),(2,1),(6,2),(7,0),(3,2),(4,8),(2,6),(0,9),(1,0),(7,4),(4,9),(1,2),(3,4),(4,1),(4,8),(1,5)]

scene1 = Scene((10,10), is_main_scene=True)
scene1.use_seperator = False
for pos in positions:
	new_entity = Entity(pos, (1,1))

before = datetime.now()
for child in scene1.children:
	child.move(DISTANCE, 0, collide=True)
col_on_time = datetime.now() - before

scene1.render()

scene2 = Scene((10,10), is_main_scene=True)
scene2.use_seperator = False
for pos in positions:
	new_entity = Entity(pos, (1,1))

before = datetime.now()
for child in scene2.children:
	child.move(DISTANCE, 0, collide=False)
col_off_time = datetime.now() - before
scene2.render()

print(f"It took {col_on_time} to move that with collisions on")
print(f"It took {col_off_time} to move that with collisions off")