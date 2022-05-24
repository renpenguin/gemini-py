import sys, os, curses

canvas = None

def end_canvas():
	"""You MUST run this function before your program ends"""
	curses.nocbreak()
	canvas.keypad(False)
	curses.echo()
	curses.endwin()

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
	>>> 	# Other processes"""
	_arrow_keys = {"A": "up","B": "down","C": "right","D": "left"}
	direction_keys = {"w":(0,-1), "a":(-1,0), "s":(0,1), "d":(1,0)}

	def __init__(self):
		self.pressed_key = self.get_key_press(False)

	def string_key(self, c: str | None) -> str:
		key = str(repr(c))[1:-1] if c else None
		if key == "\\x1b":
			if self.get_key_press() == "[":
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
					try:
						if c := sys.stdin.read(1):
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