import random
from gemini import Scene, Sprite, Entity, sleep

IS_WAIT = True
CUSTOM_TERRAIN = []
TERRAIN_WIDTH = len(CUSTOM_TERRAIN) if CUSTOM_TERRAIN else 30

scene = Scene((TERRAIN_WIDTH+1,6), is_main_scene=True, clear_char=" ")
scene.use_seperator = False

walls = []
wall_heights = CUSTOM_TERRAIN or [
    random.randint(1, 5) for _ in range(1, TERRAIN_WIDTH)
]

for i,wall_height in enumerate(wall_heights):
	wall = Entity((i+1,6-wall_height), (1,wall_height), layer=1)
	walls.append(wall)

def is_walled(pos: tuple):
	walled_left = False
	for i in range(pos[0]):
		if scene.is_entity_at((pos[0]-i, pos[1]), layers=[1]):
			walled_left = True

	walled_right = False
	for i in range(TERRAIN_WIDTH-pos[0]):
		if scene.is_entity_at((pos[0]+i, pos[1]), layers=[1]):
			walled_right = True

	return (walled_left and walled_right) or not scene.is_entity_at((pos[0],pos[1]+1))

water_count = 0

i = 0
times_since_placed = 0
while True:
	i += 1
	water = Sprite((i%TERRAIN_WIDTH,0), image="░", collisions=True)
	water_count += 1
	been_to = []
	while True:
		if water.pos[1] == 5 or not is_walled(water.pos) and water.pos[1] != 0:
			water.parent = None
			del water
			water_count -= 1
			times_since_placed += 1
			break
		if water.pos in been_to and scene.is_entity_at((water.pos[0],water.pos[1]+1)):
			times_since_placed = 0
			break
		else:
			been_to.append(water.pos)
		if water.move(0,1) == 1:
			if not scene.is_entity_at((water.pos[0]+1,water.pos[1]+1)) or not scene.is_entity_at((water.pos[0]+1,water.pos[1])):
				water.move(1,0)
			elif not scene.is_entity_at((water.pos[0]-1,water.pos[1]+1)) or not scene.is_entity_at((water.pos[0]-1,water.pos[1])):
				water.move(-1,0)
			else:
				times_since_placed = 0
				break
		if IS_WAIT:
			sleep(.01) # To watch the simulation take place
			scene.render()

	if times_since_placed > TERRAIN_WIDTH:
		break

scene.render(layers=[1])
scene.render()
print(f"There are {water_count}cm^2 of water (1cm^2 is a single character)")