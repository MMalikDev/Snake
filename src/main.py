import sys

from config import settings
from lib import player
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
        if "cli" in sys.argv:
            human = player.human.PlayerCLI(width, height)
        else:
            human = player.human.PlayerGUI(width, height)
        human.play()

    if "show" in sys.argv:
        agent = player.ai.agent.Agent(model)
        if "cli" in sys.argv:
            ai = player.ai.PlayerCLI(width, height, agent)
        else:
            ai = player.ai.PlayerGUI(width, height, agent)

        if show_graph:
            agent.model.show_summary()
        ai.play()

    if "train" in sys.argv or train:
        if "gui" in sys.argv and display:
            game = player.ai.state.StateGUI(width, height)
        elif "cli" in sys.argv:
            game = player.ai.state.StateCLI(width, height)
        else:
            game = player.ai.state.StateBase(width, height)
        agent = player.ai.agent.Agent(model)
        if show_graph:
            agent.model.show_summary()

        trainer = player.ai.Trainer(game, agent, target_score)
        trainer.train()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Snake Game was Terminated")
