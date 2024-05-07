from collections import namedtuple
from time import sleep
import requests
import multiprocessing
import math

State = namedtuple("State", "last_idle last_total")
Square = namedtuple("Square", "top_left_x top_left_y bottom_right_x bottom_right_y")

TOTAL_CPU = multiprocessing.cpu_count()
STAT_FILENAME = "/proc/stat"
THRESHOLD = 3
SQUARE_SIZE = int(math.sqrt(64*64 / TOTAL_CPU))
SQUARES_PER_ROW = int(64 / SQUARE_SIZE)
PIXOO_REST_URL = "http://localhost:5000/rectangle"
SEND_TO_PIXOO = True
CLEAR = True

def color_rectangles(results, squares, size=TOTAL_CPU):
    for i in range(size):
        if results[i] is True:
            sq = squares[i]
            data = {
                "top_left_x": sq.top_left_x,
                "top_left_y": sq.top_left_y,
                "bottom_right_x": sq.bottom_right_x,
                "bottom_right_y": sq.bottom_right_y,
                "r": 255,
                "g": 0,
                "b": 0
            }
            requests.post(PIXOO_REST_URL, data)
        else:
            sq = squares[i]
            data = {
                "top_left_x": sq.top_left_x,
                "top_left_y": sq.top_left_y,
                "bottom_right_x": sq.bottom_right_x,
                "bottom_right_y": sq.bottom_right_y,
                "r": 0,
                "g": 0,
                "b": 0
            }
            requests.post(PIXOO_REST_URL, data)

# Build Squares
squares = []
x = 0
y = 0
for i in range(4):
    ub_y = y + SQUARE_SIZE
    if i == 0:
        ub_y -= 1
    for j in range(4):
        ub_x = x + SQUARE_SIZE
        if j == 0:
            ub_x -= 1
        squares.append(Square(x+1, y+1, ub_x-1, ub_y-1))
        x = ub_x
    x = 0
    y = ub_y

print(squares)

if CLEAR:
    color_rectangles([False], [Square(0, 0, 63, 63)], size=1)

states = [State(0, 0) for i in range(TOTAL_CPU)]
results = [False for i in range(TOTAL_CPU)]
while True:
    utilisations = [0 for i in range(TOTAL_CPU)]
    with open(STAT_FILENAME) as f:
        # SKip the first line
        f.readline()
        # Read the next TOTAL_CPU lines
        for i in range(TOTAL_CPU):
            state = states[i]

            fields = [float(column) for column in f.readline().strip().split()[1:]]
            print(fields)
            idle, total = fields[3], sum(fields)

            idle_delta, total_delta = idle - state.last_idle, total - state.last_total
            states[i] = State(idle, total)
            utilisation = 100.0 * (1.0 - idle_delta / total_delta)
            utilisations[i] = utilisation
            if utilisation > THRESHOLD:
                results[i] = True
            else:
                results[i] = False

    print(utilisations)
    print(results)
    if SEND_TO_PIXOO:
        color_rectangles(results, squares)
    sleep(1)



## Other ideas:
# - [ ]  Make each square a slightly different color
# - [ ] Add padding to each square
# - [ ] Blink each square
