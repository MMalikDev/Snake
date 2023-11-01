from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchinfo

from lib.utilities import logger


class Linear_QNet(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        super().__init__()
        self.inputs = (input_size, hidden_size, output_size)
        self.layer_in = nn.Linear(self.inputs[0], self.inputs[1])
        self.layer_out = nn.Linear(self.inputs[1], self.inputs[2])

    def forward(self, x) -> nn.Linear:
        x = F.relu(self.layer_in(x))
        return self.layer_out(x)

    def show_summary(self):
        logger.info("Showing Model Summary")
        torchinfo.summary(self)

    def show_stats(self):
        logger.info("Showing Model Stats")
        for k, v in self.state_dict().items():
            logger.info("%s\t%a", k, v)

    def save(self, filepath: str) -> None:
        file = Path.cwd() / "models/Linear_QNet" / filepath
        file.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self, file)

    @staticmethod
    def load(
        filepath: str, input_size: int, hidden_size: int, output_size: int
    ) -> "Linear_QNet":
        file = Path.cwd() / "models/Linear_QNet" / filepath

        if file.exists():
            logger.info("Loading the following model: %s", filepath)
            model = torch.load(file)
            model.eval()
        else:
            logger.warning("The following model was not found: %s", filepath)
            logger.warning("Defaulting to untrained model instance")
            model = Linear_QNet(input_size, hidden_size, output_size)

        return model


class QTrainer:
    def __init__(self, model: nn.Module, lr: float, gamma: int) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model

        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done) -> None:
        # Optimize Conversion
        state = np.array(state)
        action = np.array(action)
        reward = np.array(reward)
        next_state = np.array(next_state)

        # (n, x)
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            done = (done,)

        # 1: Predicted Q values with current state
        predicted = self.model(state)

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # predicted.clone()
        # predictions[argmax(action)] = Q_new
        target = predicted.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(
                    self.model(next_state[idx])
                )

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        self.optimizer.zero_grad()

        loss = self.criterion(target, predicted)
        loss.backward()

        self.optimizer.step()
