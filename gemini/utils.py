import sys, time, math

def printd(*texts: str, delay=0.01, skip_delay_characters=[" "]):
	"""Delayed print function. A simple print function that can be used in place of the usual print to have your text print out character by character, like in text adventure games!"""
	for i in "".join(texts):
		sys.stdout.write(i)
		sys.stdout.flush()
		if i not in skip_delay_characters:
			time.sleep(delay)
	print()

def correct_position(pos: tuple[int,int], limits: tuple[int,int]=None):
	if not limits:
		limits = main_scene.size

	new_pos = list(pos)

	if len(new_pos) != 2:
		raise ValueError("Position coordinates should have exactly 2 values")

	for i in range(2):
		if limits[i]-1 < new_pos[i]:
			new_pos[i] -= limits[i]
		elif -limits[i] > new_pos[i]:
			new_pos[i] += limits[i]

	return new_pos

def add_pos(pos_a, pos_b) -> tuple[int, int]:
	return tuple(map(int.__add__, pos_a, pos_b))

class _MainScene:
	"""Helper class for main scenes"""

	def __init__(self) -> None:
		self._main_scene = None

	@property
	def main_scene(self):
		return self._main_scene

	@main_scene.setter
	def main_scene(self, value):
		self._main_scene = value
main_scene = _MainScene()

class txtcolours:
	"""txtcolours can be used to set an entity's colour, like so:
	>>> from gemini import Scene, Entity, txtcolours as tc
	>>> scene = Scene((10,10))
	>>> entity1 = Entity(pos=(3,1),size=(2,1),colour=tc.RED)

	this will make entity1 red"""
	PURPLE = '\033[95m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	COLOURS = [PURPLE, BLUE, CYAN, GREEN, YELLOW, RED]