import curses
from typing import Optional

import pygame

from lib.game import Direction, SnakeGameCLI, SnakeGameGUI
from lib.player.base import PlayerBase


class PlayerGUI(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameGUI

    def get_input(self, game: SnakeGameGUI) -> Optional[Direction]:
        steps = {
            pygame.K_UP: Direction.UP,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
        }

        for event in game.get_event():
            if event.type == pygame.KEYDOWN and event.key in steps.keys():
                return steps.get(event.key)


class PlayerCLI(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameCLI

    def get_input(self, game: SnakeGameGUI) -> Optional[Direction]:
        return {
            curses.KEY_UP: Direction.UP,
            curses.KEY_RIGHT: Direction.RIGHT,
            curses.KEY_DOWN: Direction.DOWN,
            curses.KEY_LEFT: Direction.LEFT,
        }.get(game.get_event())
