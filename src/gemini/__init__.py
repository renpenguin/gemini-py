import os
from .utils import correct_position, main_scene, txtcolours, printd, Vec2D, force_types, sleep
from .input import Input
from .camera import Camera
from . import utils

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
		return self.parent.background_tile if self.hidden else self._fill_char
	@fill_char.setter
	def fill_char(self, value: str):
		self._fill_char = value
	@property
	def pos(self):
		return Vec2D(self._pos)
	@pos.setter
	def pos(self, value: Vec2D):
		if self.parent:
			self._pos = Vec2D(correct_position(value, self.parent.size))
		else:
			self._pos = Vec2D(value)
	@property
	def all_positions(self):
		return [correct_position(self.pos + (i,j), self.parent.size) for i in range(self.size[0]) for j in range(self.size[1])]

	def __init__(self, pos: Vec2D, size: Vec2D, parent: 'Scene'=None, auto_render:bool=False, layer: int=0, fill_char:str="█", colour:str="", collisions: list[int]|bool=[], hidden:bool=False, move_functions: list=[]):
		self._parent: 'Scene' = None
		if parent := parent or main_scene.main_scene:
			self.parent = parent

		self._pos = Vec2D(0,0)
		self.pos, self.size, self.fill_char = pos, Vec2D(size), fill_char
		self.colour, self.layer = colour, layer
		self.auto_render, self.hidden = auto_render, hidden
		self.collisions: list = [-1] if collisions == True else [] if collisions == False else collisions
		self.move_functions: list[function] = move_functions

	def __str__(self):
		return f"Entity(pos={self.pos},size={self.size},fill_char='{self._fill_char}')"

	def move(self, x:int|tuple, y:int=None, collide: bool=None, run_functions=True, render: bool=None):
		"""Move the Entity within the scene. `+x` is right and `+y` is down. By enabling the Entity's auto_render property, calling this function will automatically render the scene that this Entity belongs to. If your scene is stuttering while animating, make sure you're only rendering the scene once per frame.

		When collisions are on, the entity will collide with anything that isnt the background"""
		if render is None:
			render = self.auto_render

		has_collided = False

		move = Vec2D(x, y)

		if move.x != 0 or move.y != 0:
			if collide is None:
				collide = self.collisions
			if collide:
				prev_hidden = self.hidden
				self.hidden = True

				bake = self.parent.render(False, self.collisions, False)

				def step_collide(axis: utils.Axis, p):
					if p == 0:
						return
					colliding = abs(p)
					polarity = (1 if p > 0 else -1)
					for j in range(colliding):
						for wall_p in range(self.size[0 if axis is utils.Axis.Y else 1]):
							next_pos = axis.vector( (self.size[axis.value] if p > 0 else -1) + j * polarity, wall_p )
							if self.parent.is_entity_at(self.pos + next_pos, self.collisions, bake):
								nonlocal has_collided
								colliding, has_collided = j, True

						if colliding < abs(p):
							break
					self.pos += axis.vector(colliding * polarity)

				step_collide(utils.Axis.X, move.x)
				step_collide(utils.Axis.Y, move.y)

				self.hidden = prev_hidden
			else:
				self.pos += move

			if run_functions and not has_collided:
				for func in self.move_functions:
					func()

		if render:
			self.parent.render()

		return 1 if has_collided else 0

	def get_pixel(self, pos: Vec2D) -> str:
		return self.fill_char

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

	_image = ""

	@property
	def image(self):
		"""This will return nothing if the sprite is hidden, to always get the raw image"""
		return " \n"*self.size[1] if self.hidden else self._image
	@image.setter
	def image(self, value: str):
		self._image = value
		self.size = Vec2D(len(max(value.split("\n"), key= lambda x: len(x))), value.count("\n") + 1)

	@property
	def render_image(self):
		"""Regular image but with the extra characters"""
		render_image = self.image.split("\n")
		for i, n in enumerate(self.extra_characters):
			render_image[i] += "​"*n # Add zero width spaces
		return '\n'.join(render_image)
	@property
	def all_positions(self):
		raw_positions = [
			(i,j) for i in range(self.size[0]) for j in range(self.size[1])
		]
		return [
			self.pos + pos for pos in raw_positions
			if self.get_pixel(pos) != " "
		]

	def __init__(self, pos: Vec2D, image: str, transparent: bool=True, extra_characters: list=[], *args, **kwargs):
		super().__init__(pos, (0,0), *args, **kwargs) # dummy size parameter
		self.transparent = transparent
		self.extra_characters = extra_characters
		self.image = image.strip("\n")
		del self._fill_char

	def __str__(self):
		return f"Sprite(pos={self.pos},image='{self._image[:10]}{'...' if len(self._image) > 10 else ''}')"

	def get_pixel(self, pos: Vec2D) -> str:
		try:
			return self.render_image.split("\n")[pos[1]][pos[0]]
		except Exception:
			return " "

class AnimatedSprite(Sprite):
	"""## AnimatedSprite
	The AnimatedSpite object works the same way as the Sprite class, but accepts a list of images instead of only one, and can be set which to show with the `current_frame` value. The `image` property will now return the current frame as an image

	This here will create an AnimatedSprite PacMan whose mouth will change every time the move function is used:
	>>> from gemini import Scene, AnimatedSprite
	scene = Scene((10,10))
	new_entity = AnimatedSprite((5,5), ["O","C","<","C"], parent)
	new_entities.move_functions.append(new_entity.next_frame,)
	```"""

	@property
	def current_frame(self):
		"""Returns the index of the current frame, to get a picture of the actual frame use self.image.
		When setting the current_frame, the index will always autocorrect itself to be within the fram list's range."""
		return self._current_frame
	@current_frame.setter
	def current_frame(self, value: int):
		self._current_frame = value % len(self.frames)
		self.image = self.frames[self._current_frame]

	def __init__(self, pos: Vec2D, frames: list, *args, **kwargs):
		self.frames = [frame.strip("\n") for frame in frames]
		self._current_frame = 0

		super().__init__(pos, frames[0], *args, **kwargs)

	def __str__(self):
		return f"AnimatedSprite(pos={self.pos},frames='{str(self.frames)[:20]}')"

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
	use_separator = True
	_void_char = '¶'

	@property
	def is_main_scene(self):
		return main_scene.main_scene == self
	@is_main_scene.setter
	def is_main_scene(self, value):
		main_scene.main_scene = self if value else None

	@property
	def background_tile(self):
		"""Return the background character with colours included"""
		return f"{self.bg_colour}{self.clear_char}{txtcolours.END if self.bg_colour != '' else ''}"

	def __init__(self, size: Vec2D, clear_char="░", bg_colour="", children: list[Entity]=[], render_functions: list=[], is_main_scene=False):
		self.size = size
		self.clear_char = clear_char
		self.bg_colour = bg_colour
		self.children: list[Entity] = children[:]
		self.render_functions: list[function] = render_functions

		if is_main_scene:
			self.is_main_scene = True

	def __str__(self):
		return f"Scene(size={self.size},clear_char='{self.clear_char}',is_main_scene={self.is_main_scene})"

	def get_separator(self, use_separator=None, used_lines=None):
		"""Create a use_separator to put above display so that you can only see one rendered scene at a time"""
		if use_separator is None:
			use_separator = self.use_separator

		seperator = "\n" * (os.get_terminal_size().lines - (used_lines or self.size[1]))

		return seperator if use_separator else ""

	def _render_stage(self, stage: list[list], show_coord_numbers=False, starting_coords=(0,0)):
		"""Return a baked scene, ready for printing. This will take your grid of strings and render it. You can also set `show_coord_numbers=True` to print your scene with coordinate numbers for debugging purposes"""
		if show_coord_numbers:
			for i, c in enumerate(stage, starting_coords[1]):
				c.insert(0, str(i)[-1:])
			stage.insert( 0, [' '] + [ str(starting_coords[0]+i)[-1:] for i in range(len(stage[0])-1) ] )
		return "\n".join(["".join(row) for row in stage])+"\n"

	def add_to_scene(self, new_entity: Entity):
		"""Add an entity to the scene. This can be used instead of directly defining the entity's parent, or if you want to move the entity between different scenes"""
		self.children.append(new_entity)
		new_entity._parent = self

	def render(self, is_display=True, layers: list=None, run_functions=True, *, _output=True, show_coord_numbers=False, use_separator=None):
		"""This will print out all the entities that are part of the scene with their current settings. The character `¶` can be used as a whitespace in Sprites, as regular ` ` characters are considered transparent, unless the transparent parameter is disabled, in which case all whitespaces are rendered over the background.

		When rendering an animation, make sure to put a short pause in between frames to set your fps. `gemini.sleep(0.1)` will mean a new fram every 0.1 seconds, aka 10 FPS

		If your scene is stuttering while animating, make sure you're only rendering the scene once per frame

		If the `layers` parameter is set, only entities on those layers will be rendered. Entities will also be rendered in the order of layers, with the smallest layer first

		For debugging, you can set `show_coord_numbers=True` to more see coordinate numbers around the border of your rendered scene. These numbers will not show in the render function's raw output regardless
		"""

		if run_functions:
			for function in self.render_functions:
				function()

		stage = [[self.background_tile] * self.size[0] for _ in range(self.size[1])] # Create the render 'stage'
		entity_list = list(filter(lambda x: x.layer in layers, self.children)) if layers and layers != [-1] else self.children # Get a list of the entities the user wants to render
		for entity in sorted(entity_list, key=lambda x: x.layer, reverse=True):
			extra_length = 0
			if isinstance(entity, Sprite) and entity.extra_characters:
				extra_length = max(entity.extra_characters)
			# Add each pixel of an entity to the stage
			for x in range(entity.size[0]+extra_length):
				for y in range(entity.size[1]):
					displacement = Vec2D(x, y)
					pixel = entity.get_pixel(displacement)
					if pixel == " " and hasattr(entity, "transparent") and entity.transparent:
						continue
					point = correct_position(entity.pos + displacement, self.size)
					stage[point[1]][point[0]] = f"{entity.colour}{pixel.replace(self._void_char,' ')}{txtcolours.END if entity.colour else ''}"

		if is_display:
			print(
				self.get_separator(use_separator) +
				self._render_stage(stage, show_coord_numbers)
			)
		if _output:
			return stage

	def is_entity_at(self, pos: Vec2D, layers: list=[-1], bake=None):
		"""Check for any object at a specific position, can be sorted by layers. `-1` in the layers list means to collide with all layers"""
		layers = layers if isinstance(layers, list) else [layers]
		render = bake or self.render(is_display=False, layers=None if -1 in layers else layers, run_functions=False)
		pos = correct_position(pos, self.size)
		coordinate = render[pos[1]][pos[0]]
		return coordinate != self.background_tile

	def get_entities_at(self, pos: Vec2D, layers: list[int]=[]) -> list[Entity]:
		"""Return all entities found at the chosen position, can be filtered by layer"""
		layers = layers if isinstance(layers, list) else [layers]
		layers = layers if layers != [-1] else []
		entities: list[Entity] = list(filter(lambda x: x.layer in layers, self.children)) if layers else self.children

		return list(filter(lambda x: pos in x.all_positions, entities))