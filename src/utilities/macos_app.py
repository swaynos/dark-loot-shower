import utilities.config as config
import logging
import pyscreenshot as ImageGrab
import Quartz

from AppKit import NSRunningApplication, NSWorkspace, NSApplicationActivateAllWindows, NSApplicationActivateIgnoringOtherApps

# window
class Window:
    def __init__(self):
        self.Height = int(0)
        self.Width = int(0)
        self.X = int(0)
        self.Y = int(0)

class RunningApplication():
    def __init__(self):
         self.app: NSRunningApplication = None
         self.app_name = None
         self.pid = None
         self.window = None
    
    def warm_up(self, app_name):
        self.app_name = app_name
        self.find_app(app_name)
        self.activate_app()
        self.get_window()

    def activate(self):
        self.activate_app()

    def is_app_active(self) -> bool:
        if (not self.app):
            raise ValueError("app must be set, try running find_app before calling is_app_active_frontmost")
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
        return self.app_name == active_app

    def find_app(self, appName):
        """
        Returns an application object from AppKit if the application with the given name is running, otherwise None.
        
        Args:
            appName (str): The name of the application to search for.
            
        Returns:
            NSRunningApplication or None if no such application is found.
        """
        _app = None
        # Get a list of all running applications
        apps = NSWorkspace.sharedWorkspace().runningApplications()

        # Iterate over the list of windows
        for app in apps:
            # app.bundleIdentifier() can also be used
            logging.debug(f"{app.localizedName()} - {app.processIdentifier()}")
            if (app.localizedName().lower() == appName.lower()):
                _app = app

        self.app = _app
        self.pid = _app.processIdentifier()
        return _app
    
    def activate_app(self):
        if (not self.app):
            raise ValueError("app must be set, try running find_app before activate_app")

        # app.isActive: Indicates whether the application is currently frontmost.
        if not (self.is_app_active()):
            logging.debug("{} is not active, attempting to activate.".format(config.APP_NAME))
            activationResult = self.app.activateWithOptions_(NSApplicationActivateAllWindows | NSApplicationActivateIgnoringOtherApps)

            if not (activationResult):
                raise RuntimeError("macOS app activation failed")

    def get_window(self) -> Window: 
        if (not self.pid):
            raise ValueError("app/pid must be set, try running find_app before get_window")
        
        # TODO: There is a bug if all windows from the application are minimized
        
        # Retrieve window information
        window_list = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
            Quartz.kCGNullWindowID
        )

        matched_windows = []

        # Iterate through the window list and filter by the app's PID
        for window_info in window_list:
            if window_info["kCGWindowOwnerPID"] == self.pid:
                # Extract relevant window details (e.g., window ID, title, etc.)
                window = Window()
                window.Height = int(window_info["kCGWindowBounds"]["Height"])
                window.Width = int(window_info["kCGWindowBounds"]["Width"])
                window.X = int(window_info["kCGWindowBounds"]["X"])
                window.Y = int(window_info["kCGWindowBounds"]["Y"])
                matched_windows.append(window)

        if (len(matched_windows) > 0):
            
            if (len(matched_windows) > 1):
                logging.debug("More than one matched window was found. Returning the first window.")

            self.window = matched_windows[0]
            return matched_windows[0]


    def get_image_from_window(self):
        """
        Returns an image of the given window, with any unwanted elements removed and resized to 720p resolution (1280x720).
        
        Args:
            window (NSWindow): The window object for which the image should be captured.
            
        Returns:
            A PIL Image object representing the screenshot of the given window.
        """
        if (not self.window):
            raise ValueError("window must be set, try running get_window before get_image_from_window")
        
        deltaX = self.window.X + self.window.Width
        deltaY = self.window.Y + self.window.Height
        img = ImageGrab.grab(
            backend="mac_screencapture", 
            bbox =(self.window.X, self.window.Y, deltaX, deltaY)
        )
        # Remove the top border from the image
        cropped_img = img.crop((0, config.APP_HEADER_HEIGHT, img.width, img.height))
        
        # Resize the image to 540p resolution (960x540)
        if (config.APP_RESIZE_REQUIRED):
            resized_image = cropped_img.resize((960, 540))
            final_image = resized_image
        else:
            final_image = cropped_img

        return final_image