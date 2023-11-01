from . import ai, game, gui


class Core:
    Dimension = game.Dimension()

    Display = gui.Display()
    Color = gui.Color()

    DecisionMatrix = ai.DecisionMatrix()
    TRAINER = ai.Trainer()
    States = ai.States()
    Models = ai.Models()
    Agent = ai.Agent()


settings = Core()
