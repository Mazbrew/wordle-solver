from pynput import keyboard
from pynput.keyboard import Controller, Key
from pynput.mouse import Button,Controller as MController

def pressString(guess):
    for i in range(5):
        bot.press(guess[i])
        bot.release(guess[i])

    bot.press(Key.enter)
    bot.release(Key.enter)

def restart():
    bot.press(Key.f5)

def focus(point):
    botM.position = (point[0],point[1])
    botM.press(Button.left)
    botM.release(Button.left)

bot = Controller()
botM = MController()

