from lib.utilities import load_bool, load_variable


class Dimension:
    HEIGHT = int(load_variable("HEIGHT", 24))
    WIDTH = int(load_variable("WIDTH", 32))


class Player:
    HAM: bool = load_bool("HAM") or load_bool("ham")
    HUMAN: bool = load_bool("HUMAN") or load_bool("human")
    NEURAL: bool = load_bool("NEURAL") or load_bool("neural")


class UI:
    GUI: bool = load_bool("GUI") or load_bool("gui")
    CUI: bool = load_bool("CUI") or load_bool("cui")
    CLI: bool = load_bool("CLI") or load_bool("cli")
