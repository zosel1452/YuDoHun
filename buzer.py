import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(4,GPIO.OUT)
p = GPIO.PWM(4,100)

Frq = [262,294,330,349,392,440,493,452]
speed = 0.5

p.start(10)

try:
    while 1:
        for fr in Frq:
            p.ChangeFrequency(fr)
            time.sleep(speed)

except Keyboardinterrupt:
    pass
p.stop()
GPEO.cleanup()
