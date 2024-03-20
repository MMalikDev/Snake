import collections
import functools
from typing import DefaultDict

from game import Direction, Point, SnakeGame, SnakeGameCLI, SnakeGameCUI, SnakeGameGUI
from lib.hamiltonian import HamCycle
from player.base import PlayerBase


class PlayerHam(PlayerBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.graph = HamCycle(self.width, self.height).graph
        self.food = collections.defaultdict(int)
        self.cells = width * height
        self.cost = None

        self.directions = {
            (0, -1): Direction.UP,
            (1, 0): Direction.RIGHT,
            (0, 1): Direction.DOWN,
            (-1, 0): Direction.LEFT,
        }

    def get_input(self, game: SnakeGame) -> Direction:
        if not self.food:
            self.food = game.food
            self.cost = self.calc_cost(game.food)
        if self.food == game.head:
            self.food = game.food
            self.cost = self.calc_cost(game.food)

        x, y = game.head

        moves = (
            pos
            for pos in (
                Point(x, y - 1),
                Point(x + 1, y),
                Point(x, y + 1),
                Point(x - 1, y),
            )
            if pos not in game.snake
        )

        pt = min(moves, key=lambda i: self.cost[i])
        if pt == self.graph[game.head] or self.is_safe(game, pt):
            return self.directions[pt.x - x, pt.y - y]

        pt = self.graph[game.head]
        return self.directions[pt.x - x, pt.y - y]

    def is_safe(self, game: SnakeGame, new_head: Point, food_found: int = 5) -> bool:
        """
        Looks ahead snake.length + food_found steps:
            if snake never bites it's tail when following the ham path returns True
            if snake bites its tail then the path is not safe returns False
        """

        body = game.snake.copy()
        body.appendleft(new_head)
        temp_body_set = set(body)
        for _ in range(len(body)):
            body.appendleft(self.graph[body[0]])
            if food_found > 0:
                temp_body_set.remove(body.pop())
            food_found -= 1
            if body[0] in temp_body_set:
                return False
            temp_body_set.add(body[0])
        return True

    @functools.lru_cache(None)
    def calc_cost(self, food: Point) -> DefaultDict[Point, int]:
        """Returns a map of Point -> steps to reach food if following the ham cycle"""

        cost = collections.defaultdict(lambda: self.cells)
        pt = self.graph[food]
        cost[food] = 0
        steps = 1
        while steps <= self.cells:
            cost[pt] = self.cells - steps
            pt = self.graph[pt]
            steps += 1
        return cost


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
