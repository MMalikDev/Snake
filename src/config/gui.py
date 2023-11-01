from lib.utilities import load_variable


class Color:
    BACKGROUND = load_variable("BACKGROUND_HEX_COLOR", "#000000")
    SNAKE = load_variable("SNAKE_HEX_COLOR", "#6CBB3C")
    FOOD = load_variable("FOOD_HEX_COLOR", "#ff0800")


class Display:
    BLOCK = int(load_variable("BLOCK_SIZE", 20))
    FRAMERATE = int(load_variable("FRAMERATE", 30))
    SHOW = load_variable("SHOW", "True").upper() in ["1", "TRUE"]
