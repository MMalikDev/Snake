from typing import Iterable, Tuple

from lib.game import SnakeGameGUI

from .base import StateBase


class StateGUI(StateBase, SnakeGameGUI):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def play_step(self, action: Iterable[int]) -> Tuple[int, bool, int]:
        reward, game_over, self.score = super().play_step(action)
        self.refresh()
        return reward, game_over, self.score