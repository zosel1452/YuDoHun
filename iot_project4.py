import spidev
import time

import  RPi.GPIO as GPIO

from threading import Thread
import time

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
    
    time.sleep(0.0001)

def tcp(reading):
    HOST = '192.168.0.10'
    PORT = 8888
    BUFSIZE = 1024

    while True:
        try:
            clientSocket = socket(AF_INET,SOCK_STREAM)
            clientSocket.connect((HOST,PORT))
            sleep.time(0.01)
            clientSocket.sendall(bytes("%s"%reading,'UTF-8'))
            data = clientSocket.recv(1024)
            print(data.decode())

        except Exception as e:
            print(e)
            clientSocket.close()

while True:
    reading = analog_read(0)
    voltage = reading * 3.3 / 1024
    print("Reading = %d \n Voltage = %f" %(reading, voltage))
    time.sleep(1)
    
    thread1 = Thread(target= light, args=(reading,))
    time.sleep(0.5)
    thread2 = Thread(target= tcp, args=(reading,))

    thread1.start()
    thread2.start()
