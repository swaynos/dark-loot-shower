from enum import Enum
from pynput import keyboard as kb

"""
Valid Keys
Buttons: Moon, Cross, Pyramid, Box, R1, L1, R3, L3, PS, Options, Touchpad, Share
D-Pad: Right, Down, Left, Up
Triggers: R2, L2
Sticks: Right Stick, Left Stick
"""
class Joystick():
     def __init__(self):
        self.Up = None
        self.Down = None
        self.Left = None
        self.Right = None
        
class XboxIO(kb.Controller):
    A = kb.Key.enter
    B = kb.Key.backspace
    X = kb.KeyCode(char='\\')
    Y = kb.KeyCode(char='c')
    DPadRight = kb.Key.right
    DPadDown = kb.Key.down
    DPadLeft = kb.Key.left
    DPadUp = kb.Key.up
    RB = kb.KeyCode(char='3')
    LB = kb.KeyCode(char='2')
    R3 = kb.KeyCode(char='6')
    L3 = kb.KeyCode(char='5')
    XboxButton = kb.Key.esc
    ViewButton = kb.KeyCode(char='o')
    MenuButton = kb.KeyCode(char='t')
    ShareButton = kb.KeyCode(char='f')
    LT = kb.KeyCode(char='1')
    RT = kb.KeyCode(char='4')
    Lstick = Joystick()
    Rstick = Joystick()
    def __init__(self):
        super().__init__()
        self.Lstick.Left = kb.KeyCode(char='[')
        self.Lstick.Right = kb.KeyCode(char=']')
        self.Lstick.Up = kb.KeyCode(char='w')
        self.Lstick.Down = kb.KeyCode(char='s')
        self.Rstick.Left = kb.KeyCode(char='-')
        self.Rstick.Right = kb.KeyCode(char='=')
        self.Rstick.Down = kb.Key.page_down
        self.Rstick.Up = kb.Key.page_up

    """
    Release all joystick direction.
    
    Parameters:
    -----------
    joystick: Joystick, required
        The joystick to release all directions for.
    
    Returns:
    --------
    None
    """ 
    def release_joystick_direction(self, joystick):
        self.release(joystick.Down)
        self.release(joystick.Right)
        self.release(joystick.Left)
        self.release(joystick.Up)
    
    """
    Release all buttons on the controller.
    
    Returns:
    --------
    None
    """
    def release_all_buttons(self):
        self.release(self.A)
        self.release(self.B)
        self.release(self.X)
        self.release(self.Y)
        self.release(self.DPadRight)
        self.release(self.DPadDown)
        self.release(self.DPadLeft)
        self.release(self.DPadUp)
        self.release(self.RB)
        self.release(self.LB)
        self.release(self.R3)
        self.release(self.L3)
        self.release(self.PS)
        self.release(self.XboxButton)
        self.release(self.ViewButton)
        self.release(self.MenuButton)
        self.release(self.ShareButton)
        self.release(self.LT)
        self.release(self.RT)
        self.release_joystick_direction(self.Lstick)
        self.release_joystick_direction(self.Rstick)