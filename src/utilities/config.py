# global static config
APP_NAME = "Moonlight" #"NVIDIA GeForce NOW" "steamstreamingclient"
APP_HEADER_HEIGHT = 0 #0 if fullscreen, 28 or 56 depending on DPI settings and monitor
APP_RESIZE_REQUIRED = False

CAPTURE_IMAGE_DELAY = 5 # Delay in seconds between loops of capture_image_handler

SAVE_SCREENSHOTS = True
SCREENSHOTS_DIR = "./screenshots/"
# This will save the screenshot response from Ollama only if the image has been saved
SAVE_SCREENSHOT_RESPONSE = True

LOG_LEVEL = "DEBUG"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llava"