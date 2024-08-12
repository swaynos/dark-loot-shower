import asyncio
import time
from typing import List

from src.utilities.xbox_io import XboxIO

class GameFlowController():
    def __init__(self):
        self.io = XboxIO()

    def do_something(self) -> None:
        self.io.tap(self.io.A)

    # TODO: Come up with a better way to combine multiple streams of input
    # For example, while pressing the left joystick to upper left, I also want to tap
    # A every 50 ms, and then B every 200ms. How might that input be combined in a way 
    # where the syntax doesn't get too messy?
    async def do_something_long(self, duration):
            end_time = time.time() + duration
            try:
                while time.time() < end_time:
                    # Sequence to spin in a circle
                    # Up and Left
                    with self.io.pressed(self.io.LT, self.io.Lstick.Up, self.io.Lstick.Left):
                        self.io.tap(self.io.Rstick.Left)
                        await asyncio.sleep(0.25)  # Keep it pressed for 0.25 seconds

            except asyncio.CancelledError:
                # Add any cleanup code if needed here when cancelled
                # This may be redundant
                self.io.release_joystick_direction(self.io.Lstick)
                self.io.release_joystick_direction(self.io.Rstick)
                # Notify about cancellation if needed
            finally:
                self.io.release_all_buttons() # Ensure all buttons are released
                pass