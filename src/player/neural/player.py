from typing import Optional

from game import Direction
from player.base import PlayerBase

from .agent import Agent
from .state import GameStateBase, GameStateCLI, GameStateGUI, GameStateTerm


class _PlayerRL(PlayerBase):
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        super().__init__(width, height)
        self.game = GameStateBase
        self.agent = agent

    def get_input(self, game: GameStateBase) -> Optional[Direction]:
        state = self.agent.get_state(game)
        action = self.agent.get_action(state)
        return game.get_direction(action)


class PlayerGUI(_PlayerRL):
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        super().__init__(width, height, agent)
        self.game = GameStateGUI


class PlayerCLI(_PlayerRL):
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        super().__init__(width, height, agent)
        self.game = GameStateCLI


class PlayerTerm(_PlayerRL):
    def __init__(self, width: int, height: int, agent: Agent) -> None:
        super().__init__(width, height, agent)
        self.game = GameStateTerm
