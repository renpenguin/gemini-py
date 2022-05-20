from gemini import Input, InputNew, sleep

# InputNew messes up the terminal

user_input = InputNew()
print(user_input.pressed_key*10)
user_input.stop()
sleep(2)