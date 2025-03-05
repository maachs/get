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
    val = 0
    for i in range(7, -1, -1):
        val += 2 ** i
        val_out = dec_to_bin(val)
        gpio.output(dac, val_out)
        time.sleep(0.01)
        val_in = gpio.input(comp)
        if val_in:
            val -= 2 ** i
    return val

try:
    while True:
        j = adc()
        if j != 0:
            print(f"{j}  volt = {j * 3.3 / 256}")


finally:
    gpio.output(dac, 0)
    gpio.cleanup()