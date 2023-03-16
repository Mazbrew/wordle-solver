from pynput import keyboard

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

    if key == keyboard.Key.f9:
        print("starting the execution of the program")

with keyboard.Listener(on_press=None, on_release=on_release) as listener:
    listener.join()

