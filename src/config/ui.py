from lib.utilities import load_variable


class Color:
    BACKGROUND = load_variable("BACKGROUND_HEX_COLOR", "#000000")
    SNAKE = load_variable("SNAKE_HEX_COLOR", "#6CBB3C")
    FOOD = load_variable("FOOD_HEX_COLOR", "#ff0800")


class Display:
    FRAMERATE = int(load_variable("FRAMERATE_GUI", 30))
    BLOCK = int(load_variable("BLOCK_SIZE_GUI", 20))
    DELAY = float(load_variable("DELAY_CLI", 0.1))
