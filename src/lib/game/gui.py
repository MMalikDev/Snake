import pygame

from config import settings
from lib import color

from .base import Point, SnakeGame


class SnakeGameGUI(SnakeGame):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.get_event = pygame.event.get
        self.clock = pygame.time.Clock()

        self.framerate = settings.Display.FRAMERATE
        self.block = settings.Display.BLOCK

        self.bg_color = settings.Color.BACKGROUND
        self.snake_color = settings.Color.SNAKE
        self.food_color = settings.Color.FOOD
        self.tail = None

        self.skin_color = color.lighten(self.snake_color)
        self.apple_color = color.darken(self.food_color)
        self.initialize_display()

    def initialize_display(self) -> None:
        pygame.init()
        pygame.display.set_caption("Snake")
        width, height = self.width * self.block, self.height * self.block
        self.display = pygame.display.set_mode((width, height))

    def color_cell(self, pt: Point, color: pygame.Color) -> None:
        x, y = pt.x * self.block, pt.y * self.block
        cell = pygame.Rect(x, y, self.block, self.block)
        pygame.draw.rect(self.display, color, cell)

    def color_border(self, pt: Point, color: pygame.Color) -> None:
        x, y = pt.x * self.block, pt.y * self.block
        cell = pygame.Rect(x, y, self.block, self.block)
        pygame.draw.rect(self.display, color, cell, 2)

    def render_display(self) -> None:
        self.color_cell(self.food, self.food_color)
        self.color_border(self.food, self.apple_color)

        if self.tail:
            self.color_cell(self.head, self.snake_color)
            self.color_border(self.head, self.skin_color)
        else:
            for pt in self.snake:
                self.color_cell(pt, self.snake_color)
                self.color_border(pt, self.skin_color)
            self.tail = self.snake[-1]

        if self.tail != self.snake[-1]:
            self.color_cell(self.tail, self.bg_color)
            self.tail = self.snake[-1]

    def new_game(self) -> None:
        self.display.fill(self.bg_color)
        super().new_game()

    def refresh(self) -> None:
        pygame.display.set_caption(f"Snake - Score: {self.score}")
        self.clock.tick(self.framerate)
        self.render_display()
        pygame.display.flip()

    def exit(self) -> None:
        pygame.display.quit()
        pygame.quit()
        super().exit()

    def handle_kill_switch(self) -> None:
        super().handle_kill_switch()
        for event in self.get_event():
            if event.type == pygame.QUIT:
                self.exit()
