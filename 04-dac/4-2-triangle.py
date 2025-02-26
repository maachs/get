import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

gpio.setup(dac, gpio.OUT)


def dec_to_bin(val):
    s = bin(val)[2:].zfill(8)
    return [int(bit) for bit in s]

try:
    period = float(input())

    while True:
        for i in range (0, 255):
            gpio.output(dac, dec_to_bin(i))
            time.sleep(period/512)
            print(i)

        for j in range (0, 255):
            gpio.output(dac, dec_to_bin(255 - j))
            print(255 - j)
            time.sleep(period/512)

finally:
    gpio.output(dac, 0)
    gpio.cleanup()