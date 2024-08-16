import asyncio
import time

from pynput import keyboard as kb
from typing import List

class GameFlowController():

    def do_something(self) -> None:
        # send enter
        kb.Controller.tap(kb.Key.enter)

    # TODO: Come up with a better way to combine multiple streams of input
    # For example, while pressing the left joystick to upper left, I also want to tap
    # A every 50 ms, and then B every 200ms. How might that input be combined in a way 
    # where the syntax doesn't get too messy?
    async def do_something_long(self, duration):
        end_time = time.time() + duration
        try:
            while time.time() < end_time:
                # Just garbage input to show a couple of techniques using pynput
                with kb.Controller.pressed(kb.Key.shift, kb.KeyCode(char='\\')):
                    kb.Controller.tap(kb.Key.enter)
                    await asyncio.sleep(0.25)  # Keep it pressed for 0.25 seconds

        except asyncio.CancelledError:
            # Add any cleanup code if needed here when cancelled
            # Notify about cancellation if needed
            pass
        finally:
            self.io.release_all_buttons() # Ensure all buttons are released
            pass