import sys

import player
from config import settings
from lib.utilities import debug, logger


# ---------------------------------------------------------------------- #
# Main Functions                                                         #
# ---------------------------------------------------------------------- #
# @debug
def main() -> None:
    width, height = settings.Dimension.WIDTH, settings.Dimension.HEIGHT
    target_score = settings.TRAINER.TARGET_SCORE
    show_graph = settings.TRAINER.SHOW_GRAPH
    model = settings.Models.FILEPATH
    display = settings.Display.SHOW
    train = settings.TRAINER.TRAIN

    if "human" in sys.argv:
        if "gui" in sys.argv:
            human = player.human.PlayerGUI(width, height)
        elif "cli" in sys.argv:
            human = player.human.PlayerCLI(width, height)
        else:
            human = player.human.PlayerTerm(width, height)

        human.play()

    if "ham" in sys.argv or train:
        if "gui" in sys.argv and display:
            perfect = player.hamiltonian.PlayerGUI(width, height)
        elif "cli" in sys.argv:
            perfect = player.hamiltonian.PlayerCLI(width, height)
        else:
            perfect = player.hamiltonian.PlayerTerm(width, height)

        perfect.play()

    if "show" in sys.argv:
        agent = player.neural.Agent(model)
        if show_graph:
            agent.model.show_summary()

        if "gui" in sys.argv:
            neural_net = player.neural.PlayerGUI(width, height, agent)
        elif "cli" in sys.argv:
            neural_net = player.neural.PlayerCLI(width, height, agent)
        else:
            neural_net = player.neural.PlayerTerm(width, height, agent)

        neural_net.play()

    if "train" in sys.argv or train:
        agent = player.neural.Agent(model)
        if show_graph:
            agent.model.show_summary()

        if "gui" in sys.argv and display:
            game = player.neural.GameStateGUI(width, height)
        elif "cli" in sys.argv:
            game = player.neural.GameStateCLI(width, height)
        elif "term" in sys.argv:
            game = player.neural.GameStateTerm(width, height)
        else:
            game = player.neural.GameStateBase(width, height)

        trainer = player.neural.Trainer(game, agent, target_score)

        trainer.train()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Snake Game was Terminated")
