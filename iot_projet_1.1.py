import RPi.GPIO as GPIO
import datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time ,datetime             
import RPi.GPIO as GPIO
from threading import Thread
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from socket import *
from select import select
import sys


import subprocess





flag = 0                  
count = 0
RealTime = 0

i = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



######## glober ############

cnt_time=0

first_time=0
pa_sw=0
stop_sw=0
real_time=0

####### 핀 번호창 #######
TRIG = 23
ECHO = 24
BUTT_START = 19
BUTT_STOP = 26
SENSER_ON = 21
SENSER_OFF = 20

########## HOST, PORT #######


#######################


print("Distance measurement in progress")

########  설정창 ######
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(BUTT_START,GPIO.IN)
GPIO.setup(BUTT_STOP,GPIO.IN)

GPIO.setup(SENSER_ON,GPIO.OUT)
GPIO.setup(SENSER_OFF,GPIO.OUT)

#############oled  ##########
def oled():

    global now_time
    global pa_sw
    global stop_sw
    global cnt_time


    RST = None
    Dc = 23
    SPI_PORT =0
    SPI_DEVICE = 0


    disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_address=0x3C)
    disp.begin()
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1',(width,height))
    draw = ImageDraw.Draw(image)

    draw.rectangle((0,0,width,height), outline=0,fill=0)
    padding = -2
    top = padding
    bottom = height-padding

    x = 0
    font = ImageFont.load_default()
    #font2 = ImageFont.truetype('digital-7.mono.ttf', 28)
    dateString = '%A %d %B %Y'

    try:


        while True:
            now_time = time.time()
            cnt_time = now_time - first_time

            m = (cnt_time/60)/10
            mm = (cnt_time/60)%10
            h = (m/60)/10
            hh =(h/60)%10

            strDate = datetime.datetime.now().strftime(dateString)

            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x,top),strDate, font=font,fill=255)
            draw.line((0, top+12, 127, top+12), fill=100)
            draw.text((x+20,top+14),'{0:0.0f}'.format(int(h)), font=font,fill=255)
            draw.text((x+35,top+14),'{0:0.0f} '.format(int(hh)), font=font,fill=255)
            draw.text((x+50,top+14),':', font=font,fill=255)
            draw.text((x+65,top+14),'{0:0.0f}'.format(int(m)), font=font,fill=255)
            draw.text((x+80,top+14),'{0:0.0f}'.format(int(mm)), font=font,fill=255)
            disp.image(image)
            disp.display()
            time.sleep(0.1)
            if stop_sw==1:
                print("oled  end")
                break
            if pa_sw==1:
                print("oled pause")
                while True:
                    time.sleep(1)
                    if pa_sw==2:
                        break;
    except KeyboardInterrupt:
        print("oled stop")
        GPIO.cleanup()

###############################################


###########ultira_sensor##################


def ultra_sensor_on():

    GPIO.output(TRIG,False)           
    print("waiting for sensor tho settle")   
    global stop_sw
    global pa_sw

    count_err = 0
    try:                               
        while True:                    
            GPIO.output(TRIG,True)     
            time.sleep(0.0001)
            GPIO.output(TRIG,False) 
            if count_err > 499:
                print("Sensor !!!! Error!!")
            count_err = 0
            while GPIO.input(ECHO) == 0 and count_err < 500:
                start = time.time() 
                count_err += 1

            while GPIO.input(ECHO) == 1 and count_err < 500:
                stop = time.time()         

            check_time = stop - start     
            distance = check_time*34300 / 2  
            print("%.1f"%distance)          
            time.sleep(1)

            if distance > 150:    
              #count 함수를 불러오기
              global count 
              count += 1
              if count > 10:
                  print("ERROR...!!!")
                  count = 0
            else :
                count = 0

            if stop_sw==1:
                print("sensor end")
                break
            if pa_sw==1:
                    print("sensor pause")
                    while True:
                        time.sleep(1)
                        if pa_sw==2:
                            break;
            else :
                count_sensor_error =0
    except KeyboardInterrupt:
        print("ultra sensor stop")
        GPIO.cleanup()

 #############stop##########

def stop_sensor():

    time.sleep(2)
    global stop_sw
    #여기에서 전체값 보내기####
    while True:
        if GPIO.input(26) == GPIO.HIGH:
            stop_sw=1
            break

###########pause############
def pause():

    global pa_sw
    global stop_sw
    time.sleep(2)
    while True:
        if stop_sw==1:
            break

        if GPIO.input(19) == GPIO.HIGH:
            pa_sw+=1
        if pa_sw==1:
            while True:
                time.sleep(1)
                if GPIO.input(19) == GPIO.HIGH:
                    pa_sw+=1
                    if pa_sw==2:
                        
                        time.sleep(2)
                        pa_sw=0
                        break

##########study_time##############

def study_time_count():

    count+=1

    if (count == 10):                          
        print("start")                          
        GPIO.output(SENSER_OFF,False)           
        GPIO.output(SENSER_ON,True)             

        RealTime = 0                     

####### TCP TONGSIN #########
def tcp(ttt):
    HOST = '169.254.248.1'
    PORT = 8888
    BUFSIZE = 1024
    print(ttt)

    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:

        clientSocket.connect((HOST,PORT))
        clientSocket.sendall(bytes("Data : %0.1f \n"%ttt, 'UTF-8'))
        print('Send : Hello, Server!\n')
        data = clientSocket.recv(1024)
        print(data.decode())
        clientSocket.close()

    except Exception as e:

        print(e)
        #clientSocket.close()

#####버튼을 누르면 센서작동###

ultra_on = Thread(target=ultra_sensor_on,args=())
oledsensor = Thread(target=oled,args=())
stop  = Thread(target=stop_sensor,args=())
pause_sensor = Thread(target=pause, args=())

while True:
    if GPIO.input(26) == GPIO.HIGH:    
        swich =1                      
        print("start")   
        time.sleep(0.0001)
        break
while True:
    if swich == 1 :
        first_time = time.time()
        oledsensor.start()
        ultra_on.start()
        stop.start() 
        pause_sensor.start()

        ultra_on.join()       
        oledsensor.join() 
        stop.join() 
        pause_sensor.join()

        if stop_sw==1:
            tcp(cnt_time)
        break

