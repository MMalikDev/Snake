from lib.utilities import load_bool, load_variable


class DecisionMatrix:
    KEEP_STRAIGHT = (1, 0, 0)
    TURN_RIGHT = (0, 1, 0)
    TURN_LEFT = (0, 0, 1)


class States:
    MAX_ITERATION = int(load_variable("STATES_MAX_ITERATION", 100))


class Agent:
    DEMO = load_bool("AGENT_DEMO") or load_bool("demo")
    ACTIONS = 3
    STATES = 11


class Models:
    EPSILON_BREAKPOINT = int(load_variable("MODEL_EPSILON_BREAKPOINT", 80))
    HIDDEN_LAYERS = int(load_variable("MODEL_HIDDEN_LAYERS", 256))
    MAX_MEMORY = int(load_variable("MODEL_MAX_MEMORY", 100_000))
    BATCH_SIZE = int(load_variable("MODEL_BATCH_SIZE", 1000))
    LR = float(load_variable("MODEL_LR", 0.001))

    FILEPATH: str = load_variable("MODEL_FILEPATH")


class Trainer:
    TARGET_SCORE = int(load_variable("TRAIN_TARGET_SCORE", 100))
    TRAIN_AGENT = load_bool("TRAIN_AGENT") or load_bool("train")
    SHOW_GRAPHS = load_bool("SHOW_TRAINING_GRAPHS", True)
