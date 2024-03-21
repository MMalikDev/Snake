from collections import defaultdict
from functools import lru_cache
from typing import DefaultDict, List, Optional, Set

from game import Direction, Point, SnakeGame, SnakeGameCLI, SnakeGameCUI, SnakeGameGUI
from players.base import PlayerBase


class PlayerHam(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.cells = width * height
        self.next_move = 0
        self.cycle = []

        self.edges = self.get_edges(width, height)
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

    @lru_cache(None)
    def get_edges(self, rows: int, cols: int) -> DefaultDict[Point, List[Point]]:
        """Returns an edge-list for 4-directionally connected nodes in an array of dimensions (R, C)"""
        edges = defaultdict(list)
        for r in range(rows):
            for c in range(cols):
                edge = Point(r, c)
                if r:
                    edges[edge].append(Point(r - 1, c))
                    edges[Point(r - 1, c)].append(edge)
                if c:
                    edges[edge].append(Point(r, c - 1))
                    edges[Point(r, c - 1)].append(edge)
        return edges

    def get_cycle(self, game: SnakeGame) -> List[Direction]:
        start = Point(0, 0)

        def dfs(
            node: Point, visited: Set[Point], edges: DefaultDict[Point, List[Point]]
        ) -> List[Optional[Point]]:
            nonlocal start
            if len(visited) == self.cells and start in edges[node]:
                return [start]
            for neighbor in edges[node]:
                if neighbor not in visited:
                    v = visited.copy() | {neighbor}
                    p = dfs(neighbor, v, edges)
                    if p[-1]:
                        return [neighbor] + p
            return [None]

        nodes = [start] + dfs(start, {start}, self.edges)
        cycle, n = [], len(nodes)
        for i in range(n - 1):
            pt = nodes[i]
            ptn = nodes[i + 1]
            if pt == game.head:
                self.next_move = i - 1
            direction = self.directions.get((ptn.x - pt.x, ptn.y - pt.y))
            cycle.append(direction)
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
