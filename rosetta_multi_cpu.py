from collections import namedtuple
from time import sleep

State = namedtuple("State", "last_idle last_total")

TOTAL_CPU = 16
STAT_FILENAME = "/proc/stat"

states = [State(0, 0) for i in range(TOTAL_CPU)]
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
            utilisations[i] = 100.0 * (1.0 - idle_delta / total_delta)

    print(utilisations)
    sleep(1)
