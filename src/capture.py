"""
capture.py

This script is responsible for capturing images and input of aspecified application.

Key features include:
- Captures timestamped images of the specified application
- Captures keyboard and mouse events.

Usage:
Run this script directly; it will start capturing images as per defined handler functions.
"""

import asyncio
import datetime
import logging
import signal

from utilities.shared_thread_resources import exit_event
from handlers.capture_image_handler import capture_image_handler
from utilities.input_capture import on_press, on_release, on_click
# Listeners will still be started automatically when you import the module.

from utilities.macos_app import RunningApplication
import utilities.config as config

# Configure logging for the application
# Create a unique filename with a timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f'capture_{timestamp}.log'
logging.basicConfig(level=config.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_filename, filemode='w')

# Begin Program
app = RunningApplication()
app.warm_up(config.APP_NAME)

# Define sigint/sigterm handler
def exit_handler(signum, frame):
    signal_names = {signal.SIGINT: "SIGINT", signal.SIGTERM: "SIGTERM", signal.SIGSTOP: "SIGSTOP"}
    logging.critical(f"[{signal_names[signum]}] received. Application attempting to close gracefully.")

    exit_event.set()
    
# Activate the handlers
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

async def main():
    await asyncio.gather(
        capture_image_handler(app)
    )

if __name__ == "__main__":
    asyncio.run(main())