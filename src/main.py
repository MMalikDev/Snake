import sys

import player
from config import settings
from lib.utilities import debug, logger


# ---------------------------------------------------------------------- #
# Main Functions                                                         #
# ---------------------------------------------------------------------- #
@debug
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
        elif "cui" in sys.argv:
            human = player.human.PlayerCUI(width, height)
        else:
            human = player.human.PlayerCLI(width, height)

        human.play()

    if "ham" in sys.argv or train:
        if "gui" in sys.argv and display:
            perfect = player.hamiltonian.smart.PlayerGUI(width, height)
        elif "cui" in sys.argv:
            perfect = player.hamiltonian.smart.PlayerCUI(width, height)
        else:
            perfect = player.hamiltonian.smart.PlayerCLI(width, height)

        perfect.play()

    if "show" in sys.argv:
        if "gui" in sys.argv:
            agent = player.neural.AgentGUI(width, height, model)
        elif "cui" in sys.argv:
            agent = player.neural.AgentCUI(width, height, model)
        else:
            agent = player.neural.AgentCLI(width, height, model)
        if show_graph:
            agent.model.show_summary()

        agent.play()

    if "train" in sys.argv or train:
        if "gui" in sys.argv:
            agent = player.neural.AgentGUI(width, height, model)
        elif "cui" in sys.argv:
            agent = player.neural.AgentCUI(width, height, model)
        elif "cli" in sys.argv:
            agent = player.neural.AgentCLI(width, height, model)
        else:
            agent = player.neural.Agent(width, height, model)
        if show_graph:
            agent.model.show_summary()

        trainer = player.neural.Trainer(agent, target_score)

        trainer.train()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Snake Game was Terminated")
