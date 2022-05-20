from gemini import Scene, Entity, Sprite, AnimatedSprite, Input, txtcolours as tc

age = "46"

player = AnimatedSprite((1,1),['▇','▆','▇','█'], colour=tc.RED, auto_render=True, layer=-20, collisions=[0,-5])
player.input = Input() # attach an input class to the player

def move_player():
	input = player.input.get_key_press()
	if input in ["w","a","s","d"]:
		collided = player.move(player.input.direction_keys[input])
		if collided == 0:
			player.next_frame()
	else:
		return input

# -- Scene 0 -- #
scene0_image = """██████████████████
█ █              █
█   █ █ ███ ████ █
███   █ █   █  █ █
█   ███   █   █  █
█ ███   █ █ ████ █
█     ███ █      █
█████ █   ███ ████
█                █
█                █
█     Привет
█                █
█                █
██████████████████"""
def scene0():
	scene0 = Scene((18, 14),clear_char=" ",children=[Sprite((0,0),scene0_image)])
	scene0.add_to_scene(player)

	while True:
		move_player()
		if player.pos == (17,10): break

# -- Scene 1 -- #
scene1_image = """██████████████████
█                █
█  Сегодня твой  █

█  день рождения █
█                █
██████████████████"""
def scene1():
	scene1 = Scene((18,7),clear_char=" ", children=[Sprite((0,0),scene1_image)])
	scene1.add_to_scene(player)
	player.pos = (0,3)

	while True:
		move_player()
		if player.pos == (17,3): break

# -- Scene 2 -- #
scene2_image = """██████████████████
█                █
      так что
█                █
██████████████████"""
def scene2():
	scene2 = Scene((18,5),clear_char=" ", children=[Sprite((0,0),scene2_image)])
	scene2.add_to_scene(player)
	player.pos = (0,2)

	while True:
		move_player()
		if player.pos == (17,2): break

# -- Scene 3 -- #
scene3_image = """
██████████████████

██████████████████"""
def scene3():
	scene3 = Scene((40,4),clear_char=" ", children=[
		Sprite((0,0),scene3_image),
		Entity((18,0),(22,4), fill_char="ㅤ", layer=-5)
	])
	scene3.add_to_scene(player)
	player.pos = (0,2)

	while True:
		move_player()
		if player.pos == (6,2): break

	texts: list[Sprite] = []
	i = -1
	while True:
		if player.input.get_key_press() == "d":
			i += 1
			player.next_frame()
			scene3.render()

			for text in texts:
				if text.pos == (0,0):
					text.image = text.image[1:]
				else:
					text.move((-1,0), collide=False)
			if i==0:   texts.append(Sprite((17,0), "Ты почти дошел", parent=scene3))
			if i==25:  texts.append(Sprite((17,0), "еще чуть чуть", parent=scene3))
			if i==50:  texts.append(Sprite((17,0), "Совсем немного", parent=scene3))
			if i==75:  texts.append(Sprite((17,0), "Как дела?", parent=scene3))
			if i==100: texts.append(Sprite((17,0), "У меня хорошо, я текст,", parent=scene3))
			if i==124: texts.append(Sprite((17,0), "и могу сидеть здесь", parent=scene3))
			if i==144: texts.append(Sprite((17,0), "сколько хочу", parent=scene3))
			if i==200: texts.append(Sprite((17,0), "Ладно, иди дальше", parent=scene3))
			if i==220: break

	while True:
		move_player()
		if player.pos == (17,2): break

# -- Scene 4 -- #
scene4_image = """██████████████████████████████
█                            █
      с днем рождения!       █
█                            █
█                            █
█                            █
█                            █
█                            █
█                            █
█                            █
█                            █
█                            █
██████████████████████████████"""
cake = f"""
     {age[0]} {age[1]}
     | |
/----------\\
|----------|
|vegan cake|
|__________|
\__________/"""
def scene4():
	scene4 = Scene((30,13),clear_char=" ", children=[Sprite((0,0),scene4_image), Sprite((9,3),cake, layer=1)])
	scene4.add_to_scene(player)
	player.pos = (0,2)

	while True:
		if move_player() == " ":
			break
		if scene4.get_entities_at(player.pos, layers=[1]):
			scene4.add_to_scene(Entity(player.pos, (1,1), fill_char=" ", layer=-1))

scene0()
scene1()
scene2()
scene3()
scene4()

print("\n\nС днем рождения папа :D\n\n")