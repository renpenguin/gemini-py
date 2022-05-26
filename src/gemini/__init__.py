import os
from time import sleep
from .utils import correct_position, main_scene, txtcolours, printd, add_pos
from .input import Input

# main engine file

# -- Entities --

class Entity:
	"""## Entity
	The Entity is the most basic object in a Gemini Scene. It is simply a rectangle of your chosen proportions. You can create a new entity like so.

	>>> from gemini import Scene, Entity
	>>> new_scene = Scene((30,15))
	>>> new_entity = Entity(pos=(5,4), size=(2,1), parent=new_scene)

	You can also set all entities created to have the same parent like this:
	>>> new_scene = Scene((30,15), is_main_scene=True)
	>>> new_entity = Entity((5,4), (2,1))
	"""

	@property
	def parent(self):
		return self._parent
	@parent.setter
	def parent(self, value: 'Scene'):
		if (self._parent != value or value is None) and self._parent:
			self._parent.children.remove(self)
		if value != None:
			value.add_to_scene(self)

	@property
	def fill_char(self):
		return self._fill_char if not self.hidden else self.parent.get_background()
	@fill_char.setter
	def fill_char(self, value: str):
		self._fill_char = value
	@property
	def pos(self):
		return tuple(self._pos)
	@pos.setter
	def pos(self, value: tuple[int,int]|list[int,int]):
		if len(value) != 2:
			raise ValueError("Value should be a tuple of (x,y)")
		if self.parent:
			self._pos = tuple(correct_position(value, self.parent.size))
		else:
			self._pos = tuple(value)
	@property
	def all_positions(self):
		return [add_pos(self.pos, (i,j)) for i in range(self.size[0]) for j in range(self.size[1])]

	def __init__(self, pos: tuple[int,int], size: tuple[int,int], parent: 'Scene'=None, auto_render=False, layer: int=0, fill_char="█", colour="", collisions: list[int]|bool=[], hidden=False, move_functions: list=[]):
		self._parent: 'Scene' = None
		self._pos = [0,0]
		self.pos = pos
		self.size = size
		self._fill_char = fill_char
		self.colour = colour
		self.auto_render = auto_render
		self.layer: int = layer
		self.collisions: list = [-1] if collisions == True else [] if type(collisions) == False else collisions
		self.hidden = hidden
		self.move_functions: list[function] = move_functions

		parent = parent if parent else main_scene.main_scene
		if parent:
			# parent.add_to_scene(self)
			self.parent = parent

	def __str__(self):
		return f"Entity(pos={self.pos},size={self.size},fill_char='{self._fill_char}',parent={self.parent})"

	def move(self, x:int|tuple, y:int=None, collide: bool=None, run_functions=True, render: bool=None):
		"""Move the Entity within the scene. `+x` is right and `+y` is down. By enabling the Entity's auto_render property, calling this function will automatically render the scene that this Entity belongs to. If your scene is stuttering while animating, make sure you're only rendering the scene once per frame.

		When collisions are on, the entity will collide with anything that isnt the background"""
		if collide is None:
			collide = self.collisions
		render = render or self.auto_render

		has_collided = False

		y = y if type(x) == int else x[1]
		x = x if type(x) == int else x[0]

		if x != 0 or y != 0: # Only use move code if there is something to be moved
			if run_functions:
				for func in self.move_functions:
					func()

			if collide:
				prev_hidden = self.hidden
				self.hidden = True

				x_pol = 1 if x > 0 else -1
				y_pol = 1 if y > 0 else -1

				# Move the entity as much as possible in each direction

				if x != 0:
					colliding_x = abs(x)
					for i in range(colliding_x):
						for wall_y in range(self.size[1]):
							if self.parent.is_entity_at(add_pos(self.pos, (self.size[0] if x > 0 else -1, wall_y)), layers=self.collisions):
								colliding_x, has_collided = i, True
						if colliding_x < abs(x)-1:
							break
					self.pos = add_pos(self.pos, (colliding_x * x_pol, 0))
				if y != 0:
					colliding_y = abs(y)
					for i in range(colliding_y):
						for wall_x in range(self.size[0]):
							if self.parent.is_entity_at(add_pos(self.pos, (wall_x, (self.size[1] if y > 0 else -1))), layers=self.collisions):
								colliding_y, has_collided = i, True
						if colliding_y < abs(y)-1:
							break
					self.pos = add_pos(self.pos, (0, colliding_y * y_pol))

				self.hidden = prev_hidden
			else:
				self.pos = add_pos(self.pos, (x,y))

		if render:
			self.parent.render()

		return 1 if has_collided else 0

	def show(self):
		"""Make the sprite shown"""
		self.hidden = False
	def hide(self):
		"""Make the sprite hidden"""
		self.hidden = True

class Sprite(Entity):
	"""## Sprite
	An entity with a give ASCII art that is rendered on the Scene, this can be used to put text on the scene, like so:
	>>> from gemini import Scene, Sprite
	>>> scene = Scene((13,3))
	>>> text = Sprite((1,1), image="Hello there", parent=scene, transparent=False)
	>>> scene.render()
	░░░░░░░░░░░░░
	░Hello there░
	░░░░░░░░░░░░░

	This makes it easy to put existing ascii art into whatever you're making, and move it around!

	In the event that a single character takes up two spaces (e.g. ¯\_(ツ)_/¯), you can use the extra_characters parameter, with each index of the list corresponding to the line with the extra character. For instance with a sprite with the image `¯\_(ツ)_/¯`, you would set `extra_characters=[1]`
	"""

	@property
	def image(self):
		"""This will return nothing if the sprite is hidden, to always get the raw image"""
		return self._image if not self.hidden else " \n"*self.size[1]
	@image.setter
	def image(self, value: str):
		self._image = value

	def __init__(self, pos: tuple, image: str, transparent: bool=True, parent: 'Scene'=None, auto_render=False, layer: int=0, colour: str="", collisions: list=[], hidden=False, move_functions: list=[], extra_characters: list=[]):
		self._image = image
		self.transparent = transparent
		self.extra_characters = extra_characters

		size = (len(max(image.split("\n"), key= lambda x: len(x))), image.count("\n") + 1)

		super().__init__(pos, size, parent, auto_render, layer, None, colour, collisions, hidden, move_functions)
		del self._fill_char

	def __str__(self):
		return f"Sprite(pos={self.pos},size={self.size},image='{self._image[:10]}{'...' if len(self._image) > 10 else ''}',parent={self.parent})"

class AnimatedSprite(Sprite):
	"""## AnimatedSprite
	The AnimatedSpite object works the same way as the regular Sprite, but accepts a list of images instead of only one, and can be set which to show with the `current_frame` value"""

	@property
	def current_frame(self, image=False):
		"""Returns the index of the current frame, to get a picture of the actual frame use self.image.

		When setting the current_frame, the index will always autocorrect itself to be within the fram list's range"""
		return self._current_frame
	@current_frame.setter
	def current_frame(self, value: int):
		self._current_frame = value
		if value < 0:
			self._current_frame = len(self.frames)-1
		elif value > len(self.frames)-1:
			self._current_frame = 0
		self.image = self.frames[self._current_frame]

	@property
	def max_frame(self):
		"""returns the largest possible frame"""
		return len(self.frames)-1
	def __init__(self, pos: tuple, frames: list, transparent: bool = True, parent: 'Scene' = None, auto_render=False, layer=0, colour: str = "", collisions: list = [], hidden=False, move_functions: list=[], extra_characters: list = []):
		self.frames = frames
		self._current_frame = 0
		self.current_frame
		super().__init__(pos, frames[0], transparent, parent, auto_render, layer, colour, collisions, hidden, move_functions, extra_characters)

	def next_frame(self):
		self.current_frame += 1

# -- Scene --

class Scene:
	"""## Scene
	You can attach entities to this scene and render the scene to display them. There can be more than one scene that can be rendered one after the other. Create a scene like so:
	>>> from gemini import Scene
	>>> new_scene = Scene((30,15))

	The width and height parameters are required and define the size of the rendered scene. To set the scene size to be the current terminal size, by using `os.get_terminal_size()`

	Using is_main_scene=True is the same as
	>>> from gemini import Scene, set_main_scene
	>>> new_scene = Scene((10,10))
	>>> set_main_scene(new_scene)

	The `render_functions` parameter is to be a list of functions to run before any render, except when the `run_functions` parameter is set to False"""
	use_seperator = True
	_void_char = '¶'

	@property
	def is_main_scene(self):
		return main_scene.main_scene == self
	@is_main_scene.setter
	def is_main_scene(self, value):
		main_scene.main_scene = self if value else None

	def __init__(self, size:tuple, clear_char="░", bg_colour="", children: list[Entity]=[], render_functions: list=[], is_main_scene=False):
		self.size = size
		self.clear_char = clear_char
		self.bg_colour = bg_colour
		self.children: list[Entity] = children[:]
		self.render_functions: list[function] = render_functions

		if is_main_scene:
			self.is_main_scene = True

	def __str__(self):
		return f"Scene(size={self.size},clear_char='{self.clear_char}',is_main_scene={self.is_main_scene})"

	def add_to_scene(self, new_entity: Entity):
		"""Add an entity to the scene. This can be used instead of directly defining the entity's parent, or if you want to move the entity between different scenes"""
		self.children.append(new_entity)
		new_entity._parent = self

	def render(self, is_display=True, layers: list=None, run_functions=True, _output=True):
		"""This will print out all the entities that are part of the scene with their current settings. The character `¶` can be used as a whitespace in Sprites, as regular ` ` characters are considered transparent, unless the transparent parameter is disabled, in which case all whitespaces are rendered over the background.

		When rendering an animation, make sure to put a short pause in between frames to set your fps. `gemini.sleep(0.1)` will mean a new fram every 0.1 seconds, aka 10 FPS

		If your scene is stuttering while animating, make sure you're only rendering the scene once per frame

		If the `layers` parameter is set, only entities on those layers will be rendered. Entities will also be rendered in the order of layers, with the smallest layer first
		"""
		if run_functions:
			for function in self.render_functions:
				function()

		seperator = "\n" * (os.get_terminal_size().lines - self.size[1]) if self.use_seperator else "" # Create a seperator to put above display so that you can only see one rendered scene at a time
		stage = [[self.get_background()] * self.size[0] for _ in range(self.size[1])] # Create the render 'stage'

		entity_list = list(filter(lambda x: x.layer in layers, self.children)) if layers else self.children # Get a list of the entities the user wants to render
		for entity in sorted(entity_list, key=lambda x: x.layer, reverse=True):
			# Code to manually handle ascii characters that can't be monospaced
			extra_length = 0
			if isinstance(entity, Sprite):
				entity_image = entity.image.split("\n")
				for i, n in enumerate(entity.extra_characters):
					entity_image[i] += "​"*n # Add zero width spaces
				entity_image = '\n'.join(entity_image)
				extra_length = max(entity.extra_characters) if entity.extra_characters else 0

			for x in range(entity.size[0]+extra_length):
				for y in range(entity.size[1]):
					# Add each pixel of an entity to the stage
					if isinstance(entity, Sprite):
						try:
							pixel = entity_image.split("\n")[y][x]
						except:
							pixel = " "
						if pixel == " " and entity.transparent:
							continue
					elif isinstance(entity, Entity):
						pixel = entity.fill_char

					point = [entity.pos[0]+x, entity.pos[1]+y]
					point = correct_position(point, self.size)
					stage[point[1]][point[0]] = f"{entity.colour}{pixel.replace(self._void_char,' ')}{txtcolours.END if entity.colour else ''}"

		if is_display:
			print(seperator+"\n".join(["".join(row) for row in stage])+"\n") # Render the stage
		if _output:
			return stage

	def get_background(self):
		"""Return the background character with colours included"""
		return f"{self.bg_colour}{self.clear_char}{txtcolours.END if self.bg_colour != '' else ''}"

	def is_entity_at(self, pos: tuple, layers: list=[-1]):
		"""Check for any object at a specific position, can be sorted by layers. `-1` in the layers list means to collide with all layers"""
		layers = layers if isinstance(layers, list) else [layers]
		render = self.render(is_display=False, layers=None if -1 in layers else layers, run_functions=False)
		pos = correct_position(pos, self.size)
		coordinate = render[pos[1]][pos[0]]
		return coordinate != self.get_background()

	def get_entities_at(self, pos: tuple[int, int], layers: list[int]=[]) -> list[Entity]:
		layers = layers if isinstance(layers, list) else [layers]
		entities: list[Entity] = list(filter(lambda x: x.layer in layers, self.children)) if layers else self.children

		return list(filter(lambda x: pos in x.all_positions, entities))


if __name__ == "__main__":
	print("This is the module file, please use a provided example instead")