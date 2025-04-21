# config.py
COLORS = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255),
    "eraser": (0, 0, 0),
}

BRUSH_SHAPES = {
    "line": "line",
    "star": "star",
    "circle": "circle"
}

DEFAULT_BRUSH_COLOR = (0, 0, 255)
DEFAULT_BRUSH_THICKNESS = 15
DEFAULT_ERASER_THICKNESS = 50
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
SMOOTHING_HISTORY = 5
RAINBOW_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
STICKER_SIZE = 50
SOUND_FILES = {
    "draw": "assets/laugh.wav",
    "erase": "assets/erase.wav",
    "clear": "assets/clear.wav",
}