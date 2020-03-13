import spidev
import time

import  RPi.GPIO as GPIO

led_A = 21
led_B = 20
led_C = 16
###############

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_A,GPIO.OUT)
GPIO.setup(led_B,GPIO.OUT)
GPIO.setup(led_C,GPIO.OUT)
###############

GPIO.output(led_A,0)
GPIO.output(led_B,0)
GPIO.output(led_C,0)


delay = 0.5


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000

def analog_read(channel):
    r = spi.xfer2([1,(8 + channel) << 4,0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out


def light(reading):    
    if (reading > 350):
        GPIO.output(led_A,1)
        GPIO.output(led_B,0)
        GPIO.output(led_C,0)

    if ( reading <= 350 and reading > 100 ):
        GPIO.output(led_A,1)
        GPIO.output(led_B,1)
        GPIO.output(led_C,0)

    if ( reading <= 100):
        GPIO.output(led_A,1)
        GPIO.output(led_B,1)
        GPIO.output(led_C,1)



while True:
    reading = analog_read(0)
    voltage = reading * 3.3 / 1024
    print("Reading = %d \n Voltage = %f" %(reading, voltage))
    time.sleep(1)
    light(reading)


