import RPi.GPIO as gpio
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

gpio.setmode(gpio.BCM)

gpio.setup(dac, gpio.OUT)
gpio.setup(leds, gpio.OUT)
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

def Volume(val):
    val = int(val/256 * 10)
    array = [0]*8
    for i in range(val - 1):
        array[i] = 1
    return array

try:
    while True:
        j = adc()
        if j != 0:
            val_vol = Volume(j)
            gpio.output(leds, val_vol)
            print(f"{j}  volt = {j * 3.3 / 256}")


finally:
    gpio.output(dac, 0)
    gpio.cleanup()