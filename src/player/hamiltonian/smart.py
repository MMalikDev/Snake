from typing import List

from game import Direction, Point, SnakeGame, SnakeGameCLI, SnakeGameCUI, SnakeGameGUI
from lib.hamiltonian import HamCycle
from player.base import PlayerBase


class PlayerHam(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.cells = width * height
        self.next_move = 0
        self.cycle = []

        self.directions = {
            (0, -1): Direction.UP,
            (1, 0): Direction.RIGHT,
            (0, 1): Direction.DOWN,
            (-1, 0): Direction.LEFT,
        }

    def get_input(self, game: SnakeGame) -> Direction:
        if not self.cycle:
            self.cycle = self.get_cycle(game)

        self.next_move += 1
        self.next_move %= self.cells
        return self.cycle[self.next_move]

    def get_cycle(self, game: SnakeGame) -> List[Direction]:
        ham = HamCycle(game.width, game.height)
        graph = ham.graph

        cycle, n = [], len(graph)
        pt = Point(0, 0)
        for i in range(n):
            ptn = graph[pt]
            if pt == game.head:
                self.next_move = i - 1
            direction = self.directions[(ptn.x - pt.x, ptn.y - pt.y)]
            cycle.append(direction)
            pt = ptn
        return cycle


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
