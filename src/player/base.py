from abc import abstractmethod
from typing import Optional

from game import Direction, SnakeGame
from lib.utilities import logger


class PlayerBase:
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width
        self.alive = True

        # Adjust based on user interface
        self.game = SnakeGame

    @abstractmethod
    def get_input(self, game: SnakeGame) -> Optional[Direction]:
        """
        Translate user inputs to Direction
        """
        pass

    def play(self) -> None:
        game = self.game(self.width, self.height)
        game.new_game()
        while self.alive:
            direction = self.get_input(game)
            self.alive = game.move(direction)
            game.refresh()
        logger.info("Final Score: %i", game.score)
        game.exit()
