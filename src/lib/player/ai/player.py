import curses
from typing import Optional

from lib.game import Direction
from lib.utilities import logger

from .agent import Agent
from .state import StateCLI, StateGUI


class PlayerGUI:
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        self.height = height
        self.width = width
        self.agent = agent

        self.alive = True
        self.game = StateGUI

    def get_input(self, game: StateGUI) -> Optional[Direction]:
        state = self.agent.get_state(game)
        action = self.agent.get_action(state)
        return game.get_direction(action)

    def play(self) -> None:
        game = self.game(self.width, self.height)
        game.new_game()
        while self.alive:
            direction = self.get_input(game)
            self.alive = game.move(direction)
            game.refresh()
        logger.info("Final Score: %i", game.score)
        game.exit()


class PlayerCLI:
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        self.height = height
        self.width = width
        self.agent = agent

        self.alive = True
        self.game = StateCLI

    def get_input(self, game: StateGUI) -> Optional[Direction]:
        state = self.agent.get_state(game)
        action = self.agent.get_action(state)
        return game.get_direction(action)

    def play(self) -> None:
        game = self.game(self.width, self.height)
        game.new_game()
        while self.alive:
            direction = self.get_input(game)
            self.alive = game.move(direction)
            game.refresh()
        logger.info("Final Score: %i", game.score)
        game.exit()
