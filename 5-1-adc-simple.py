import RPi.GPIO as gpio
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

gpio.setmode(gpio.BCM)

gpio.setup(dac, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial = gpio.HIGH)
gpio.setup(comp, gpio.IN)

def dec_to_bin(val):
    return [int(bit) for bit in bin(val)[2:].zfill(8)]

def adc():
    for i in range(256):
        val_out = dec_to_bin(i)
        gpio.output(dac, val_out)
        val_in = gpio.input(comp)
        time.sleep(0.01)
        if val_in:
            return i

    return 0

try:
    while True:
        j = adc()
        if j != 0:
            print(f"{j}  volt = {j * 3.3 / 256}")


finally:
    gpio.output(dac, 0)
    gpio.cleanup()