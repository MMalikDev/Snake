from config import settings
from game import Direction, SnakeGame, SnakeGameCLI, SnakeGameCUI, SnakeGameGUI
from lib.hamiltonian import HamCycle
from players.base import PlayerBase


class PlayerHam(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.max_size = settings.HamCycle.SUBSECTION_SIZE
        self.shuffle = settings.HamCycle.SHUFFLE

        self.cycle = HamCycle(
            self.width,
            self.height,
            max_size=self.max_size,
            shuffle=self.shuffle,
        )
        self.graph = self.cycle.graph

        self.directions = {
            (0, -1): Direction.UP,
            (1, 0): Direction.RIGHT,
            (0, 1): Direction.DOWN,
            (-1, 0): Direction.LEFT,
        }

    def get_input(self, game: SnakeGame) -> Direction:
        x, y = game.head
        pt = self.graph[game.head]
        return self.directions[pt.x - x, pt.y - y]


class PlayerGUI(PlayerHam):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameGUI


class PlayerCUI(PlayerHam):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameCUI


class PlayerCLI(PlayerHam):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameCLI
