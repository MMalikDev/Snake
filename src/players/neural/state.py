from typing import Iterable, Optional, Tuple

from config import settings
from game import Direction, SnakeGame, SnakeGameCLI, SnakeGameCUI, SnakeGameGUI


class GameStateBase(SnakeGame):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.max_iteration = settings.States.MAX_ITERATION
        self.steps = [
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
        ]

        self.reset()

    def reset(self) -> None:
        self.new_game()
        self.frame_iteration = 0

    def get_direction(self, action: Iterable[int]) -> Optional[Direction]:
        i = self.steps.index(self.direction)
        return {
            settings.DecisionMatrix.KEEP_STRAIGHT: self.steps[i],
            settings.DecisionMatrix.TURN_RIGHT: self.steps[((i + 1) % 4)],
            settings.DecisionMatrix.TURN_LEFT: self.steps[((i - 1) % 4)],
        }.get(tuple(action))

    def game_over(self) -> bool:
        too_slow = self.frame_iteration > self.max_iteration * len(self.snake)
        return self.is_collision() or too_slow

    def play_step(self, action: Iterable[int]) -> Tuple[int, bool, int]:
        self.frame_iteration += 1
        reward = 0

        direction = self.get_direction(action)
        self.move_head(direction)

        if game_over := self.game_over():
            reward = -10
            return reward, game_over, self.score

        if self.update_tail():
            self.score += 1
            reward = 10

        return reward, game_over, self.score


class GameStateGUI(GameStateBase, SnakeGameGUI):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def play_step(self, action: Iterable[int]) -> Tuple[int, bool, int]:
        reward, game_over, self.score = super().play_step(action)
        self.refresh()
        return reward, game_over, self.score


class GameStateCUI(GameStateBase, SnakeGameCUI):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def play_step(self, action: Iterable[int]) -> Tuple[int, bool, int]:
        reward, game_over, self.score = super().play_step(action)
        self.refresh()
        return reward, game_over, self.score


class GameStateCLI(GameStateBase, SnakeGameCLI):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def play_step(self, action: Iterable[int]) -> Tuple[int, bool, int]:
        reward, game_over, self.score = super().play_step(action)
        self.refresh()
        return reward, game_over, self.score
