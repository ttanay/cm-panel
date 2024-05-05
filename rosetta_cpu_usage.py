from __future__ import print_function
import math
from time import sleep
import serial

arduino = serial.Serial(port="/dev/ttyACM0", baudrate=19200, timeout=0.1)

last_idle = last_total = 0
while True:
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    utilisation = 100.0 * (1.0 - idle_delta / total_delta)
    print('%5.1f%%' % utilisation, end='\r')
    led_brightness = bytes(str(math.ceil(utilisation * 2.55)), 'utf-8')
    print(led_brightness)
    arduino.write(led_brightness)
    sleep(1)

