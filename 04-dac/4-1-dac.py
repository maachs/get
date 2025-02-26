import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

gpio.setup(dac, gpio.OUT)

def dec_to_bin(val):
    return [int(bit) for bit in bin(val)[2:].zfill(8)]

try:
    while True:
        num = input()
        try:
            num = int(num)
            if 0 <= num <= 255:
                volt = num / 255 * 3.2
                print(f"volage {volt:.4}")
                gpio.output(dac, dec_to_bin(num))
            else:
                print("num out of range")
        except Exception:
            if num == "q":
                break

finally:
    gpio.output(dac, 0)
    gpio.cleanup()
