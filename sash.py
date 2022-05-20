from gemini import Scene, Sprite

sash = '\n'.join([' '*i*4+"█"*5 for i in range(20)])

print(sash)

scene = Scene((40,20), is_main_scene=True)
for i in range(4):
	sash_sprite1 = Sprite((i*2,i*3), sash)

scene.render()