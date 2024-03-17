class TerminalTooSmall(Exception):
    def __init__(
        self,
        min_width: int,
        min_height: int,
        current_width: int,
        current_height: int,
    ):
        self.min_width = min_width
        self.min_height = min_height
        self.current_width = current_width
        self.current_height = current_height
        self.message = "Terminal is too small - Need: %iw %ih | Have: %iw %ih"

    def __str__(self):
        return self.message % (
            self.min_width,
            self.min_height,
            self.current_width,
            self.current_height,
        )
