from gemini import Scene, Entity, txtcolours as tc

scene = Scene((10,10), is_main_scene=True)
block = Entity((3,2), (4,3))

scene.render()
print(block.all_positions)

block2 = Entity(block.all_positions[-1], (1,1), colour=tc.RED)
scene.render()