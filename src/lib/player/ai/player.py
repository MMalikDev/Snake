from typing import Optional

from lib.game import Direction, SnakeGame
from lib.player.base import PlayerBase

from .agent import Agent
from .state import StateCLI, StateGUI


class _PlayerAI(PlayerBase):
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        super().__init__(width, height)
        self.game = SnakeGame
        self.agent = agent

    def get_input(self, game: StateGUI) -> Optional[Direction]:
        state = self.agent.get_state(game)
        action = self.agent.get_action(state)
        return game.get_direction(action)


class PlayerGUI(_PlayerAI):
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        super().__init__(width, height, agent)
        self.game = StateGUI


class PlayerCLI(_PlayerAI):
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        super().__init__(width, height, agent)
        self.game = StateCLI
