import datetime
import logging

from pynput import keyboard, mouse

# Create a separate logger for keyboard and mouse events
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
event_logger = logging.getLogger('EventLogger')
event_log_filename = f'events_{timestamp}.csv'
event_handler = logging.FileHandler(event_log_filename)

# Set up a CSV format for the logger
csv_formatter = logging.Formatter('%(asctime)s, %(message)s')
event_handler.setFormatter(csv_formatter)

event_logger.addHandler(event_handler)
event_logger.setLevel(logging.INFO)
event_logger.propagate = False  # Prevent logging to the root logger as well

def on_press(key):
    try:
        event_logger.info(f'key_press,{key.char}')
    except AttributeError:
        event_logger.info(f'key_press,{key}')

def on_release(key):
    event_logger.info(f'key_release,{key}')
    if key == keyboard.Key.esc:
        return False

def on_click(x, y, button, pressed):
    action = 'pressed' if pressed else 'released'
    event_logger.info(f'mouse_{action},{x},{y},{button}')
    
    if button == mouse.Button.right:
        return False

# Start the keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

# Start the mouse listener
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()