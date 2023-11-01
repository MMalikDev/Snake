import curses
from typing import Optional

import pygame

from lib.game import Direction, SnakeGameCLI, SnakeGameGUI
from lib.utilities import logger


class PlayerGUI:
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width
        self.alive = True
        self.game = SnakeGameGUI
        self.steps = {
            pygame.K_UP: Direction.UP,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
        }

    def get_input(self, game: SnakeGameGUI) -> Optional[Direction]:
        for event in game.get_event():
            if event.type == pygame.KEYDOWN and event.key in self.steps.keys():
                return self.steps[event.key]

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
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width
        self.alive = True
        self.game = SnakeGameCLI
        self.steps = {
            curses.KEY_UP: Direction.UP,
            curses.KEY_RIGHT: Direction.RIGHT,
            curses.KEY_DOWN: Direction.DOWN,
            curses.KEY_LEFT: Direction.LEFT,
        }

    def get_input(self, game: SnakeGameGUI) -> Optional[Direction]:
        event = game.get_event()
        if event in self.steps.keys():
            return self.steps[event]

    def play(self) -> None:
        game = self.game(self.width, self.height)
        game.new_game()
        while self.alive:
            direction = self.get_input(game)
            self.alive = game.move(direction)
            game.refresh()
        logger.info("Final Score: %i", game.score)
        game.exit()
