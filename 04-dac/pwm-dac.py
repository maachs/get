import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT)

n = 10
p = gpio.PWM(24, 1000)
p.start(0)

try:
    while True:
        f = int(input())
        p.ChangeDutyCycle(f)
        print(3.3 * f/ 100)
    
finally:
    p.stop()
    gpio.output(24, 0)
    gpio.cleanup()