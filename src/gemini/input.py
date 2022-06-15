import contextlib, sys, os
from .utils import Vec2D, MorphDict

class Input:
	"""## Input
	The input class is used to collect inputs from the user. To wait for a key press before continuing the code use `Input().wait_for_key_press()`
	>>> from gemini import Input
	>>> if Input().wait_for_key_press() == "g":
	>>> 	print("You pressed the right key!")

	For while loops with a wait function where you want to also check for inputs, call the input class directly after the wait function:
	>>> while True:
	>>> 	sleep(0.1)
	>>> 	input = Input().pressed_key
	>>> 	# Other processes

	you can also compare your input to `Input.direction_keys` to get a vector, so you can do this!
	>>> my_input = Input()
	>>> entity.move(my_entity.get_key_press())

	and the Entity will move in your chosen direction!
	"""
	_arrow_keys = {"A": "up","B": "down","C": "right","D": "left"}
	direction_keys = MorphDict(
		(["w","up_arrow"],Vec2D(0,-1)),
		(["s","down_arrow"],Vec2D(0,1)),
		(["a","left_arrow"],Vec2D(-1,0)),
		(["d","right_arrow"],Vec2D(1,0))
	)

	def __init__(self):
		self.pressed_key = self.get_key_press(False)

	def string_key(self, c: str | None) -> str:
		key = repr(c)[1:-1] if c else None
		if key == "\\x1b" and self.get_key_press() == "[":
			key = f"{self._arrow_keys[self.get_key_press()]}_arrow"
		return key

	def get_key_press(self, is_wait=True) -> str:
		import termios, fcntl
		fd = sys.stdin.fileno()

		oldterm = termios.tcgetattr(fd)
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

		try:
			if is_wait:
				while True:
					with contextlib.suppress(IOError):
						if c := sys.stdin.read(1):
							return self.string_key(c)
			else:
				with contextlib.suppress(IOError):
					c = sys.stdin.read(1)
					return self.string_key(c)
		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)