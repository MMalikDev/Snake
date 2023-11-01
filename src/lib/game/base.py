import random
import sys
from collections import namedtuple
from enum import Enum
from typing import Optional

import keyboard

from lib.utilities import logger

Point = namedtuple("Point", "x, y")


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class SnakeGame:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.direction = Direction.RIGHT

    def new_game(self) -> None:
        self.score = 0
        self.food = None
        self.direction = self.direction
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [
            self.head,
            Point(self.head.x - 1, self.head.y),
            Point(self.head.x - 2, self.head.y),
        ]
        self.place_food()

    def place_food(self) -> None:
        while not self.food or self.food in self.snake:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.food = Point(x, y)

    def is_collision(self, pt: Optional[Point] = None) -> bool:
        if not pt:
            pt = self.head
        if pt in self.snake[1:]:
            logger.debug("Snake ate itself...")
            return True
        if not 0 <= pt.x < self.width or not 0 <= pt.y < self.height:
            logger.debug("Boundary was hit...")
            return True
        return False

    def move(self, direction: Optional[Direction]) -> bool:
        self.move_head(direction)
        if self.is_collision():
            return False
        self.update_tail()
        return True

    def move_head(self, direction: Optional[Direction] = None) -> None:
        self.handle_kill_switch()
        x, y = self.head.x, self.head.y

        if direction:
            self.direction = direction
        match self.direction:
            case Direction.UP:
                self.head = Point(x, y - 1)
            case Direction.RIGHT:
                self.head = Point(x + 1, y)
            case Direction.DOWN:
                self.head = Point(x, y + 1)
            case Direction.LEFT:
                self.head = Point(x - 1, y)
        self.snake.insert(0, self.head)

    def update_tail(self) -> bool:
        if self.head == self.food:
            self.score += 1
            self.place_food()
            return True
        self.snake.pop()
        return False

    def exit(self) -> None:
        sys.exit()

    def handle_kill_switch(self) -> None:
        if keyboard.is_pressed("q"):
            logger.info("Kill switch utilized to exit program")
            self.exit()
