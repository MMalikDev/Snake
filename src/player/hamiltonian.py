from collections import defaultdict
from functools import lru_cache
from typing import DefaultDict, List, Tuple

from game import Direction, SnakeGame, SnakeGameCLI, SnakeGameGUI, SnakeGameTerm
from player.base import PlayerBase


class PlayerBase(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.cells = width * height
        self.next_move = 0
        self.cycle = []

    def get_input(self, game: SnakeGame) -> Direction:
        if not self.cycle:
            self.cycle = self.get_cycle(game)

        self.next_move += 1
        self.next_move %= self.cells
        return self.cycle[self.next_move]

    @lru_cache(None)
    def get_edges(
        self, rows: int, cols: int
    ) -> DefaultDict[Tuple[int, int], List[Tuple[int, int]]]:
        """Returns an edge-list for 4-directionally connected nodes in an array of dimensions (R, C)"""
        edges = defaultdict(list)
        for r in range(rows):
            for c in range(cols):
                edge = (r, c)
                if r:
                    edges[edge].append((r - 1, c))
                    edges[(r - 1, c)].append(edge)
                if c:
                    edges[edge].append((r, c - 1))
                    edges[(r, c - 1)].append(edge)
        return edges

    def get_cycle(self, game: SnakeGame) -> List:
        R, C = game.height, game.width
        N = self.cells
        start = (0, 0)

        def dfs(
            node: Tuple[int, int], visited: set, edges: List[Tuple[int, int]]
        ) -> List[Tuple[int, int]]:
            nonlocal N, start
            if len(visited) == N and start in edges[node]:
                return [start]
            for neigh in edges[node]:
                if neigh not in visited:
                    v = visited.copy() | {neigh}
                    p = dfs(neigh, v, edges)
                    if p[-1] != -1:
                        return [neigh] + p
            return [-1]

        @lru_cache(None)
        def find_cycle(R: int, C: int):
            # Build edge list
            edges = self.get_edges(R, C)
            start = (0, 0)
            result = [start] + dfs(start, {start}, edges)
            return result

        nodes = find_cycle(R, C)
        cycle, n = [], len(nodes)
        directions = {
            (0, -1): Direction.UP,
            (1, 0): Direction.RIGHT,
            (0, 1): Direction.DOWN,
            (-1, 0): Direction.LEFT,
        }

        for i in range(1, n):
            y1, x1 = nodes[i - 1]
            y2, x2 = nodes[i]
            if (y1, x1) == (game.head.y, game.head.x):
                self.next_move = i - 2
            direction = directions[(x2 - x1, y2 - y1)]
            cycle.append(direction)

        return cycle


class PlayerGUI(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameGUI


class PlayerCLI(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameCLI


class PlayerTerm(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.game = SnakeGameTerm
