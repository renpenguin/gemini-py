import sys

print(sys.path)

from gemini import Scene, AnimatedSprite, sleep

scene = Scene((14,5), is_main_scene=True)
# scene.use_seperator = False
animated = AnimatedSprite((2,2), frames=['▁'*10, '▃'*10, '▄'*10, '▅'*10, '▆'*10, '▇'*10, '█'*10])

scene.render_functions = [lambda: sleep(.2)]
i = -1
while True:
	i += 1
	animated.current_frame += 1 if i%13 < 6 else -1 if i%13 > 6 else 0
	scene.render()