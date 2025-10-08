SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Color:
    BLACK = "#16161d"
    GREEN = "#66cd00"
    RED = "#dc143c"
    AQUAMARINE = "#458b74"
    BLUE = "#53868b"
    WHITE = "#fffaf0"
    GREY = "#838b8b"

# GRAPH SETTINGS
GRAPH_X = 60
GRAPH_WIDTH = SCREEN_WIDTH - 2 * GRAPH_X
GRAPH_Y = 100
GRAPH_HEIGHT = 200
GRAPH_CORNER_ROUNDING = 6
CANDLE_WIDTH = 8
CANDLE_SPACING = 10
CANDLE_LINE_WIDTH = 2

# high factor is for making sure the graph does not go over the top, and low is to keep it from going under bottom
HIGH_FACTOR = 1.1
LOW_FACTOR = 0.85
