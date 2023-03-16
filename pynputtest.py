from pynput import keyboard
from pynput.keyboard import Key, Controller

def on_release(key):
    bot = Controller()
    
    if key == keyboard.Key.esc:
        # Stop listener
        return False

    if key == keyboard.Key.f9:
        bot.press('h')
        bot.release('h')

with keyboard.Listener(on_press=None, on_release=on_release) as listener:
    listener.join()

