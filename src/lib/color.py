import colorsys
from typing import Tuple


def hex_to_hsv(hex: str) -> Tuple[int, int, int]:
    rgb = (int(hex[i : i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hsv(*rgb)


def hsv_to_hex(h: int, s: int, v: int) -> str:
    rgb = colorsys.hsv_to_rgb(h, s, v)
    color = (min(round(c * 255), 255) for c in rgb)
    return "#{:0>2x}{:0>2x}{:0>2x}".format(*color)


def darken(hex: str, amount: float = 0.8) -> str:
    h, s, v = hex_to_hsv(hex)
    s *= amount
    v *= amount
    return hsv_to_hex(h, s, v)


def lighten(hex, amount=0.8):
    h, s, v = hex_to_hsv(hex)
    s = min(s * (amount + 1), 1)
    v = max(v * (amount + 1), 0)
    return hsv_to_hex(h, s, v)
