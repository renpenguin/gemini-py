import sys, time, enum

class MorphDict:
	"""## MorphDict
	A dictionary that can have multiple keys for one value"""
	def __init__(self, *items: dict|list[tuple]):
		if type(items) is dict:
			items = dict.items()

		self.items = [([keys] if isinstance(keys, str|int) else list(keys), value) for keys, value in items]
	def __repr__(self):
		return self.items
	def __str__(self):
		return f"{self.items}"

	def keys(self):
		return [i[0] for i in self.items]
	def all_keys(self):
		return sum(self.keys(), start=[])
	def values(self):
		return [i[1] for i in self.items]

	def __getitem__(self, i):
		return list(filter(lambda x: i in x[0], self.items))[0][1]
	def __setitem__(self, i, value):
		list(filter(lambda x: i in x[0], self.items))[0][1] = value

	def append(self, keys, value):
		self.items.append(([keys] if isinstance(keys, str|int) else list(keys), value))

class Axis(enum.Enum):
	"""Helper class for the move function. """
	X = 0
	Y = 1

	def vector(self, value, seconday_value=0) -> tuple: # My dad helped me with this :D
		"""Useful for movements in single directions"""
		match self:
			case Axis.X:
				return Vec2D(value, seconday_value)
			case Axis.Y:
				return Vec2D(seconday_value, value)

def printd(*texts: str, delay=0.01, skip_delay_characters=[" "]):
	"""Delayed print function. A simple print function that can be used in place of the usual print to have your text print out character by character, like in text adventure games!"""
	for i in "".join(texts):
		sys.stdout.write(i)
		sys.stdout.flush()
		if i not in skip_delay_characters:
			time.sleep(delay)
	print()

def sleep(secs: float):
	"""Delay execution for a given amount seconds"""
	time.sleep(secs)

def parametrized(dec):
	"""Parameters for wrapper functions, like
	`@yourwrapper(param=True)`"""
	def layer(*args, **kwargs):
		def repl(f):
			return dec(f, *args, **kwargs)
		return repl
	return layer

@parametrized
def force_types(func, skip=0, ignore_types=[]):
	"""Force function types

	`*args` should be fully hinted. Class functions (starting with self parameter) do not yet work"""
	def wraps(*args, **kwargs):
		args = list(args)
		keys_list = list(func.__annotations__.keys())
		for i, a in enumerate(args[skip:], skip-1):
			arg_type = func.__annotations__[keys_list[i]]
			if callable(arg_type) and arg_type not in ignore_types:
				args[i] = arg_type(a)

		for k,v in kwargs.items():
			if k in func.__annotations__:
				arg_type = func.__annotations__[k]
				if callable(arg_type):
					kwargs[k] = arg_type(v)
		return func(*args, **kwargs)
	wraps.__unwrapped__ = func
	return wraps

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

	def __repr__(self) -> str:
		return self.main_scene
	def __str__(self) -> str:
		return str(self.main_scene)
main_scene = _MainScene()

# Vec2D

def add_pos(pos_a,pos_b, effect=int.__add__, limits: tuple[int, int]=None):
	"""Add two vectors together.

	WARNING: This functions is deprecated, and will be removed in a future release"""
	return correct_position(map(effect, pos_a, pos_b), limits) if limits else Vec2D.__add__(pos_a, pos_b)

class Vec2D:
	"""Helper class for positions and sizes. A set of two ints. Can be initalised with `Vec2D(5,4)` or with `Vec2D([5,4])` Can also just be a replacement for `tuple[int,int]`

	Other examples:
	>>> Vec2D(5, 2) + Vec2D(4, -1)
	Vec2D(9, 1)
	>>> Vec2D(10, 10) - Vec2D(4,1)
	Vec2D(6, 9)"""

	def __init__(self, x: list|int, y:int=None):
		self.y = int(x[1] if isinstance(x, list|tuple|Vec2D) else y)
		self.x = int(x[0] if isinstance(x, list|tuple|Vec2D) else x)

	def __repr__(self):
		return (self.x, self.y)
	def __str__(self):
		return str(self.__repr__())
	def __getitem__(self, i: int):
		if i > 1:
			raise IndexError("Vec2D has no elements outside of x and y")
		return self.__repr__()[i]
	def __add__(self, value: 'Vec2D'):
		return Vec2D(list(map(int.__add__, self, value)))
	def __sub__(self, value: 'Vec2D'):
		return Vec2D(list(map(int.__sub__, self, value)))
	def __mul__(self, value: int):
		return Vec2D(self.x*value,self.y*value)
	def __truediv__(self, value: int):
		return Vec2D(self.x/value,self.y/value)
	def __eq__(self, value: 'Vec2D') -> bool:
		return self.__repr__() == Vec2D(value).__repr__()

	def normalised(self):
		return Vec2D([i/abs(i) for i in self])

@force_types()
def correct_position(pos: Vec2D, limits: Vec2D=None):
	"""Correct a position, if the position is outside the limits it will be looped back to the other side"""
	if not limits:
		limits = main_scene.size

	new_pos = list(map(
		lambda a,b: b % a if a > 0 else a,
		list(pos), limits
	))

	return Vec2D(new_pos)

class txtcolours:
	"""txtcolours can be used to set an entity's colour, like so:
	>>> from gemini import Scene, Entity, txtcolours as tc
	>>> scene = Scene((10,10))
	>>> entity1 = Entity(pos=(3,1),size=(2,1),colour=tc.RED)

	this will make entity1 red.

	Important note: for windows users please use colorama, as `txtcolours` only works with ANSI terminals. You can use `colorama.Fore.RED` instead of `txtcolours.RED`!"""

	def txt_mod(self):
		return f'\x1b[{self}m'

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