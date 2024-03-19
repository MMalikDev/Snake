from config import settings
from lib import graph
from lib.utilities import logger

from .agent import Agent


class Trainer:
    def __init__(self, agent: Agent, target_score: int) -> None:
        self.agent = agent
        self.width = agent.width
        self.height = agent.height
        self.target_score = target_score
        self.state = agent.game(self.width, self.height)

        self.total_score = 0
        self.score, self.mean_score = 0, 0
        self.record, self.mean_record = 0, 0
        self.plot_scores, self.plot_mean_scores = [], []

        self.size = "%iw%ih/" % (self.width, self.height)
        self.best = "%s/best/" % self.size
        self.steadfast = "%s/mean/" % self.size

    def remember(self) -> None:
        self.state.reset()
        self.agent.n_games += 1
        self.agent.train_long_memory()

    def update_stats(self) -> None:
        self.total_score += self.score
        self.mean_score = round(self.total_score / self.agent.n_games, 2)
        self.record = max(self.record, self.score)
        self.mean_record = max(self.mean_record, self.score)

        self.plot_scores.append(self.score)
        self.plot_mean_scores.append(self.mean_score)

    def save_model(self, path: str, num: int) -> None:
        file_name = "%s/%i.bin" % (path, num)
        self.agent.model.save(file_name)

    def save_best(self) -> None:
        if self.score >= self.record >= self.target_score:
            self.save_model(self.best, self.score // 10 * 10)

    def save_steadfast(self) -> None:
        if self.mean_score >= self.mean_record >= self.target_score:
            self.save_model(self.steadfast, self.mean_score // 10 * 10)

    def show_progress(self) -> None:
        message = "Game %i: Score %i | Record: %i"
        logger.debug(message, self.agent.n_games, self.score, self.record)
        graph.plot(self.plot_scores, self.plot_mean_scores, self.record)

    def train(self) -> None:
        while True:
            # Get old state
            stateOld = self.agent.get_state(self.state)
            # Get move
            move = self.agent.get_action(stateOld)
            # Perform move
            reward, done, self.score = self.state.play_step(move)
            # Get new state
            state_new = self.agent.get_state(self.state)
            # Remember
            self.agent.remember(stateOld, move, reward, state_new, done)
            # Train short memory
            self.agent.train_short_memory(stateOld, move, reward, state_new, done)

            if done:
                self.remember()
                self.update_stats()
                self.save_best()
                self.save_steadfast()
                if settings.TRAINER.SHOW_GRAPH:
                    self.show_progress()
