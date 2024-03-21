import players
from config import settings
from lib.utilities import debug, logger


# ---------------------------------------------------------------------- #
# Main Functions                                                         #
# ---------------------------------------------------------------------- #
@debug
def main() -> None:
    width, height = settings.Dimension.WIDTH, settings.Dimension.HEIGHT
    target_score = settings.TRAINER.TARGET_SCORE
    model = settings.Models.FILEPATH

    if settings.Player.HAM:
        player = players.hamiltonian.smart
    elif settings.Player.HUMAN:
        player = players.human
    elif settings.Player.NEURAL:
        player = players.neural

    if settings.Player.HAM or settings.Player.HUMAN:
        if settings.UI.GUI:
            game = player.PlayerGUI(width, height)
        elif settings.UI.CUI:
            game = player.PlayerCUI(width, height)
        else:
            game = player.PlayerCLI(width, height)

        game.play()

    if settings.Player.NEURAL:
        if settings.UI.GUI:
            agent = player.AgentGUI(width, height, model)
        elif settings.UI.CUI:
            agent = player.AgentCUI(width, height, model)
        elif settings.UI.CLI:
            agent = player.AgentCLI(width, height, model)
        else:
            agent = player.Agent(width, height, model)

        if settings.TRAINER.SHOW_GRAPHS:
            agent.model.show_summary()

        if settings.TRAINER.TRAIN_AGENT:
            trainer = players.neural.Trainer(agent, target_score)
            trainer.train()

        if settings.Agent.DEMO:
            agent.play()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Snake Game was Terminated")
