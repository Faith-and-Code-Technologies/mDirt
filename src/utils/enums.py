from enum import IntEnum


class BlockFace(IntEnum):
    TOP = 0
    LEFT = 1
    BACK = 2
    RIGHT = 3
    FRONT = 4
    BOTTOM = 5


class ElementPage(IntEnum):
    HOME = 0
    BLOCKS = 1
    RECIPES = 2
    ITEMS = 3
    PAINTINGS = 4
    PROJECT_SETUP = 5
    SETTINGS = 6
    STRUCTURES = 7
    ENCHANTMENTS = 8
