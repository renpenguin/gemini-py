from . import utils

class Camera:
	"""## Camera
	An object to render a specific area of a scene. It will center on the location you set, or track any entity you choose

	>>> from gemini import Scene, Entity, Camera
	>>> scene = Scene((20,10), is_main_scene=True)
	>>> block = Entity((6,3), (3,3))
	>>> camera = Camera((0,0), (5,5), focus_object=block)
	>>> scene.render(use_separator=False) # renders scene as usual
	>>> camera.render(use_separator=False) # renders scene from camera"""
	@property
	def pos(self):
		return self.focus_object.pos + self.focus_object.size/2 if self.focus_object else self._pos
	@pos.setter
	def pos(self, value: utils.Vec2D):
		self._pos = value
		self.focus_object = None # not sure about this

	# @utils.force_types(skip=1)
	def __init__(self, pos: utils.Vec2D, size: utils.Vec2D, focus_object=None, scene=None):
		self.pos = pos
		self.size = size
		self.focus_object = focus_object

		if not scene:
			scene = utils.main_scene.main_scene
		self.scene = scene

	def render(self, is_display=True, *args, _output=True, show_coord_numbers=False, use_separator=None, **kwargs):
		"""Render a scene through a camera. All `Scene.render` parameters can be used"""

		image = self.scene.render(False, *args, **kwargs)

		top_left = tuple(map(lambda x,y: x-int(y/2), self.pos, self.size))
		bot_right = tuple(map(lambda x,y: x+int(y/2) + y % 2, self.pos, self.size))

		cut_vertical = image[max(top_left[1],0):bot_right[1]]
		stage = [
			l[max(top_left[0],0):bot_right[0]] for l in cut_vertical
		]

		separator = self.scene.get_separator(use_separator, len(stage))

		if is_display:
			print(top_left)
			print(separator+self.scene._render_stage(stage, show_coord_numbers, top_left))
		if _output:
			return stage