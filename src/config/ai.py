from lib.utilities import load_variable


class DecisionMatrix:
    KEEP_STRAIGHT = (1, 0, 0)
    TURN_RIGHT = (0, 1, 0)
    TURN_LEFT = (0, 0, 1)


class States:
    MAX_ITERATION = int(load_variable("MAX_ITERATION", 100))


class Agent:
    STATES = 11
    ACTIONS = 3


class Models:
    EPSILON_BREAKPOINT = int(load_variable("EPSILON_BREAKPOINT", 80))
    HIDDEN_LAYERS = int(load_variable("HIDDEN_LAYERS", 256))
    MAX_MEMORY = int(load_variable("MAX_MEMORY", 100_000))
    BATCH_SIZE = int(load_variable("BATCH_SIZE", 1000))
    LR = float(load_variable("LR", 0.001))

    FILEPATH: str = load_variable("FILEPATH")


class Trainer:
    SHOW_GRAPH = load_variable("SHOW_GRAPH", "1").upper() in ["1", "TRUE"]
    TRAIN = load_variable("TRAIN", "").upper() in ["1", "TRUE"]
    TARGET_SCORE = int(load_variable("TARGET_SCORE", 100))
