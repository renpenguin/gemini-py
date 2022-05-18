from gemini import Scene, Sprite, txtcolours as tc

board = Scene((10,10), is_main_scene=True)
walls = Sprite((0,0), image="""██████████
█        █
█        █
█        █
█        █
█        █
█        █
█        █
█        █
██████████""")

board.render()