from enum import IntEnum

class BlockFace(IntEnum):
    TOP = 0
    LEFT = 1
    BACK = 2
    RIGHT = 3
    FRONT = 4
    BOTTOM = 5

class ElementPage(IntEnum):
    BLOCKS = 1
    RECIPES = 2
    ITEMS = 3
    PAINTINGS = 4
    PROJECT_SETUP = 5
    HOME = 0
    SETTINGS = 6