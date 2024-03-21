from . import game, hamiltonian, neural, ui


class Core:
    Dimension = game.Dimension()
    Player = game.Player()
    UI = game.UI()

    Display = ui.Display()
    Color = ui.Color()

    HamCycle = hamiltonian.HamCycle()

    DecisionMatrix = neural.DecisionMatrix()
    TRAINER = neural.Trainer()
    States = neural.States()
    Models = neural.Models()
    Agent = neural.Agent()


settings = Core()
