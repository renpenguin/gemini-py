import sys, time, enum

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
		new_pos[i] = new_pos[i] % limits[i]

	return new_pos

def add_pos(pos_a,pos_b, effect=int.__add__,limits: tuple[int, int]=None) -> tuple[int, int]:
	r = map(effect, pos_a, pos_b)
	if limits:
		return tuple(correct_position(r, limits))
	else:
		return tuple(r)

class Vec2D:
	"""Helper class for positions and sizes"""
	def __init__(self, x: tuple|int, y:int=None):
		self.y = y if type(x) == int else x[1]
		self.x = x if type(x) == int else x[0]

	def __str__(self):
		return str(self.__repr__())

	def __repr__(self):
		return (self.x, self.y)

	def __getitem__(self, i):
		if i > 1:
			raise IndexError("Vec2D has no elements outside of x and y")
		return self.__repr__()[i]

	def __add__(self, value):
		return add_pos(self, value)

	def __sub__(self, value):
		return add_pos(self, value, int.__sub__)

print(Vec2D(5,1)-Vec2D(1,2))

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

	def __str__(self) -> str:
		return str(self.main_scene)

	def __repr__(self) -> str:
		return self.main_scene
main_scene = _MainScene()

class txtcolours(enum.Enum):
	"""txtcolours can be used to set an entity's colour, like so:
	>>> from gemini import Scene, Entity, txtcolours as tc
	>>> scene = Scene((10,10))
	>>> entity1 = Entity(pos=(3,1),size=(2,1),colour=tc.RED)

	this will make entity1 red"""

	def txt_mod(id: int):
		return f'\033[{id}m'

	END = txt_mod(0)
	BOLD = txt_mod(1)
	LIGHT = txt_mod(2)
	ITALIC = txt_mod(3)
	UNDERLINE = txt_mod(4)
	INVERTED = txt_mod(7)
	CROSSED = txt_mod(9)

	ALT_GREY, GREY, INVERTED_GREY = txt_mod(30), txt_mod(90), txt_mod(40)
	ALT_RED, RED, INVERTED_RED = txt_mod(31), txt_mod(91), txt_mod(41)
	ALT_GREEN, GREEN, INVERTED_GREEN = txt_mod(32), txt_mod(92), txt_mod(42)
	ALT_YELLOW, YELLOW, INVERTED_YELLOW = txt_mod(33), txt_mod(93), txt_mod(43)
	ALT_BLUE, BLUE, INVERTED_BLUE = txt_mod(34), txt_mod(94), txt_mod(44)
	ALT_PURPLE, PURPLE, INVERTED_PURPLE = txt_mod(35), txt_mod(95), txt_mod(45)
	ALT_CYAN, CYAN, INVERTED_CYAN = txt_mod(36), txt_mod(96), txt_mod(46)

	COLOURS = [RED, GREEN, YELLOW, BLUE, PURPLE, CYAN]
	ALT_COLOURS = [ALT_RED, ALT_GREEN, ALT_YELLOW, ALT_BLUE, ALT_PURPLE, ALT_CYAN]
	INVERTED_COLOURS = [INVERTED_RED, INVERTED_GREEN, INVERTED_YELLOW, INVERTED_BLUE, INVERTED_PURPLE, INVERTED_CYAN]
	ALL_COLOURS = COLOURS + ALT_COLOURS

print(txtcolours.RED)
print(txtcolours['RED'])