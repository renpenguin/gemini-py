import sys, os

class Input:
	"""## Input
	The input class is used to collect inputs from the user. To wait for a key press before continuing use `Input().wait_for_key_press()`
	>>> from gemini import Inout
	>>> if Input().wait_for_key_press() == "g":
	>>> 	print("You pressed the right key!") """
	keys = {
		"A": "up",
		"B": "down",
		"C": "right",
		"D": "left"
	}

	def __init__(self):
		self.pressed_key = self.get_key_press(False)

	def string_key(self, c: str | None) -> str:
		key = str(repr(c))[1:-1] if c else None
		if key == "\\x1b":
			if self.get_key_press() == "[":
				key = f"{self.keys[self.get_key_press()]}_arrow"
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
					try:
						c = sys.stdin.read(1)
						if c:
							return self.string_key(c)
					except IOError: pass
			else:
				try:
					c = sys.stdin.read(1)
					return self.string_key(c)
				except IOError: pass
		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)