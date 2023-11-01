import random
from collections import deque
from typing import List, Optional

import numpy as np
import torch

from config import settings
from lib.game import Direction, Point

from .model import Linear_QNet, QTrainer
from .state import StateBase


class BaseAgent:
    def __init__(self, model: Optional[str] = None) -> None:
        self.n_games = 0
        self.epsilon = 0  # Randomness
        self.gamma = 0.9  # Discount Rate

        self.LR = settings.Models.LR
        self.STATES = settings.Agent.STATES
        self.ACTIONS = settings.Agent.ACTIONS
        self.MAX_MEMORY = settings.Models.MAX_MEMORY
        self.batch_size = settings.Models.BATCH_SIZE
        self.HIDDEN_LAYERS = settings.Models.HIDDEN_LAYERS

        self.model = self.get_model(model)
        self.memory = deque(maxlen=self.MAX_MEMORY)
        self.trainer = QTrainer(self.model, lr=self.LR, gamma=self.gamma)

    def get_model(self, model: Optional[str]) -> Linear_QNet:
        configs = (self.STATES, self.HIDDEN_LAYERS, self.ACTIONS)
        return Linear_QNet.load(model, *configs) if model else Linear_QNet(*configs)

    def remember(self, state, action, reward, next_state, done) -> None:
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done) -> None:
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self) -> None:
        if len(self.memory) > self.batch_size:
            mini_sample = random.sample(self.memory, self.batch_size)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, done = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, done)


class Agent(BaseAgent):
    def __init__(self, model: Optional[str] = None) -> None:
        super().__init__(model)
        self.epsilon_breakpoint = settings.Models.EPSILON_BREAKPOINT

    def get_action(self, state) -> List[int]:
        # random moves: tradeoff exploration / exploitation
        self.epsilon = self.epsilon_breakpoint - self.n_games
        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def get_state(self, game: StateBase):
        head = game.snake[0]

        food_up = game.food.y < game.head.y
        food_right = game.food.x > game.head.x
        food_down = game.food.y > game.head.y
        food_left = game.food.x < game.head.x

        move_up = game.direction == Direction.UP
        move_right = game.direction == Direction.RIGHT
        move_down = game.direction == Direction.DOWN
        move_left = game.direction == Direction.LEFT

        point_up = Point(head.x, head.y - 1)
        point_right = Point(head.x + 1, head.y)
        point_down = Point(head.x, head.y + 1)
        point_left = Point(head.x - 1, head.y)

        danger_straight = (
            (move_up and game.is_collision(point_up))
            or (move_right and game.is_collision(point_right))
            or (move_down and game.is_collision(point_down))
            or (move_left and game.is_collision(point_left))
        )
        danger_right = (
            (move_up and game.is_collision(point_right))
            or (move_right and game.is_collision(point_down))
            or (move_down and game.is_collision(point_left))
            or (move_left and game.is_collision(point_up))
        )
        danger_left = (
            (move_up and game.is_collision(point_left))
            or (move_right and game.is_collision(point_up))
            or (move_down and game.is_collision(point_right))
            or (move_left and game.is_collision(point_down))
        )

        state = [
            # Danger direction
            danger_straight,
            danger_right,
            danger_left,
            # Movement direction
            move_up,
            move_right,
            move_down,
            move_left,
            # Food location
            food_up,
            food_right,
            food_down,
            food_left,
        ]

        return np.array(state, dtype=int)
