import curses
from curses import textpad

from config import settings
from lib.exceptions import TerminalTooSmall

from .base import Point, SnakeGame


class SnakeGameCUI(SnakeGame):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.framerate = settings.Display.FRAMERATE
        self.tail = None

        self.initialize_display()
        self.get_event = self.display.getch

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, -1, -1)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)

        self.bg_color = curses.color_pair(1)
        self.food_color = curses.color_pair(2)
        self.snake_color = curses.color_pair(3)

    def init_sizes(self):
        h, w = self.display.getmaxyx()
        min_w, min_h = self.width + 2, self.height + 3
        self.w_offset = w // 2 - self.width // 2
        self.h_offset = h // 2 - self.height // 2 + 1
        if w < min_w or h < min_h:
            raise TerminalTooSmall(min_w, min_h, w, h)

    def initialize_display(self) -> None:
        self.display = curses.initscr()
        curses.noecho()
        curses.curs_set(False)
        self.init_sizes()
        self.init_colors()
        self.display.keypad(True)
        self.display.nodelay(True)
        self.display.timeout(self.framerate)

    def color_cell(self, pt: Point, icon) -> None:
        self.display.addch(pt.y + self.h_offset, pt.x + self.w_offset, " ", icon)

    def render_display(self) -> None:
        self.color_cell(self.food, self.food_color)

        if self.tail:
            self.color_cell(self.head, self.snake_color)
        else:
            for pt in self.snake:
                self.color_cell(pt, self.snake_color)
            self.tail = self.snake[-1]

        if self.tail != self.snake[-1]:
            self.color_cell(self.tail, self.bg_color)
            self.tail = self.snake[-1]

    def new_game(self) -> None:
        self.display.clear()
        textpad.rectangle(
            self.display,
            self.h_offset - 1,
            self.w_offset - 1,
            self.height + self.h_offset,
            self.width + self.w_offset,
        )
        super().new_game()

    def refresh(self) -> None:
        score_text = "Score: {}".format(self.score)
        h, w = 0, self.display.getmaxyx()[1] // 2 - len(score_text) // 2
        self.display.addstr(h, w, score_text)
        self.render_display()
        self.display.refresh()

    def exit(self) -> None:
        self.display.keypad(False)
        curses.curs_set(True)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        super().exit()

    def handle_kill_switch(self) -> None:
        if self.get_event() == ord("q"):
            self.exit()
