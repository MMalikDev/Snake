import curses
from typing import Optional

import pygame

from game import Direction, SnakeGameCLI, SnakeGameGUI, SnakeGameTerm
from player.base import PlayerBase


class PlayerGUI(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameGUI

    def get_input(self, game: SnakeGameGUI) -> Optional[Direction]:
        for event in game.get_event():
            if event.type == pygame.KEYDOWN:
                return {
                    pygame.K_UP: Direction.UP,
                    pygame.K_RIGHT: Direction.RIGHT,
                    pygame.K_DOWN: Direction.DOWN,
                    pygame.K_LEFT: Direction.LEFT,
                }.get(event.key)


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


class PlayerTerm(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.height = height
        self.width = width
        self.alive = True
        self.game = SnakeGameTerm

    def get_input(self, game: SnakeGameGUI) -> Optional[Direction]:
        return {
            game.display.KEY_LEFT: Direction.LEFT,
            game.display.KEY_RIGHT: Direction.RIGHT,
            game.display.KEY_UP: Direction.UP,
            game.display.KEY_DOWN: Direction.DOWN,
        }.get(game.get_event().code)
