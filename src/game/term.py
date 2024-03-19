from blessed import Terminal

from config import settings
from lib.exceptions import TerminalTooSmall

from .base import Point, SnakeGame


class SnakeGameTerm(SnakeGame):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.speed = settings.Display.FRAMERATE // 100
        self.display = Terminal()
        self.tail = None

        self.color_food = self.display.on_red
        self.color_snake = self.display.on_green

        self.color_bg = self.display.on_black
        self.border_color = self.display.on_gray

        self.initialize_display()

    def get_event(self):
        with self.display.cbreak():
            return self.display.inkey(timeout=self.speed)

    def init_sizes(self):
        h, w = self.display.height, self.display.width
        min_w, min_h = self.width + 2, self.height + 6
        self.w_offset = w // 2 - self.width // 2
        self.h_offset = h // 2 - self.height // 2 + 1
        if w < min_w or h < min_h:
            raise TerminalTooSmall(min_w, min_h, w, h)

    def initialize_display(self) -> None:
        self.init_sizes()

    def display_cell(self, pt: Point, color) -> None:
        x, y = pt.x + self.w_offset, pt.y + self.h_offset
        with self.display.location():
            print(self.display.move_yx(y, x) + (color(" ")))

    def render_display(self) -> None:
        self.display_cell(self.food, self.color_food)

        if self.tail:
            self.display_cell(self.head, self.color_snake)
        else:
            for pt in self.snake:
                self.display_cell(pt, self.color_snake)
            self.tail = self.snake[-1]

        if self.tail != self.snake[-1]:
            self.display_cell(self.tail, self.color_bg)
            self.tail = self.snake[-1]

    def display_grid(self) -> None:
        boundary = self.border_color(" ")

        horizontal = (self.width + 1) * boundary
        top = Point(self.h_offset - 1, self.w_offset)
        bottom = Point(self.h_offset + self.height, self.w_offset)

        vertical = range(self.h_offset - 1, self.h_offset + self.height + 1)
        left = [Point(self.w_offset - 1, i) for i in vertical]
        left += [Point(self.w_offset - 2, i) for i in vertical]
        right = [Point(self.width + self.w_offset, i) for i in vertical]
        right += [Point(self.width + self.w_offset + 1, i) for i in vertical]

        with self.display.location():
            print(self.display.move_yx(top.x, top.y) + horizontal)
            for pt in left:
                print(self.display.move_yx(pt.y, pt.x) + boundary)
            for pt in right:
                print(self.display.move_yx(pt.y, pt.x) + boundary)
            print(self.display.move_yx(bottom.x, bottom.y) + horizontal)

    def new_game(self) -> None:
        print(self.color_bg(self.display.clear))
        self.display_grid()
        super().new_game()

    def refresh(self) -> None:
        score_text = "Score: %i" % self.score
        center = self.display.width // 2 - len(score_text)
        with self.display.location():
            print(self.display.move_yx(1, center) + (self.color_bg(score_text)))
            self.render_display()

    def exit(self) -> None:
        print(self.display.normal)
        print(self.display.clear)
        super().exit()

    def handle_kill_switch(self) -> None:
        with self.display.cbreak():
            if self.display.inkey(timeout=0) == "q":
                self.exit()
