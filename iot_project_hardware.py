#-*-coding:utf-8-*-       #한글 사용 가능

import RPi.GPIO as GPIO 
import time               # 실시간 timer 기능 사용 라이브러리 

flag = 0                  # 
flag_1 = 0
count = 0
RealTime = 0

i = 0
ERR_ARRDIS = []

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

####### 핀 번호창 #######
TRIG = 23
ECHO = 24
BUTT_START = 19
BUTT_STOP = 26
SENSER_ON = 21
SENSER_OFF = 20


#######################


print("Distance measurement in progress")

########  설정창 ######
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(BUTT_START,GPIO.IN)
GPIO.setup(BUTT_STOP,GPIO.IN)

GPIO.setup(SENSER_ON,GPIO.OUT)
GPIO.setup(SENSER_OFF,GPIO.OUT)
#######################

while True:                            #while문 26번 핀에 입력값 들어오길 기다림
    if GPIO.input(26) == GPIO.HIGH:    #26번 핀에 값이 들어오면(버튼을 누르면)
        
        flag = 1                       #밑에 if문에 들어가기 위한 flag 변수
        print("start")   
        break                          #flag에 1값을 주고 while문 나가기
    time.sleep(0.0001)          

if (flag) == 1:                        #위에서 flag 1값, if문에 들어간다
    GPIO.output(SENSER_OFF,True)       #빨간불 키는 핀을 true
    GPIO.output(SENSER_ON,False)       #초록불 키는 핀을 false
    GPIO.output(TRIG,False)            #초음파 센서 trig 설정
    print("waiting for sensor tho settle")   
    time.sleep(2)

    try:                               #자연스럽게 try문으로 들어오고

        while True:                    #while문 시작

            GPIO.output(TRIG,True)     #초음파 센서 trig 설정
            time.sleep(0.0001)
            GPIO.output(TRIG,False)    

            while GPIO.input(ECHO) == 0:
                start = time.time()        #time.time()을 하면 시간 값나옴
            while GPIO.input(ECHO) == 1:
                stop = time.time()         #start - stop 하면 초음파 센서가 나갔다 들어오는 시간을 알 수있음

            check_time = stop - start      #초음파가 나가고 들어가는 시간
            distance = check_time*34300 / 2  #거리 = 시간*속력 (거리가 왔다갔다 거리라 절반으로 /2 를 해주면 물체 사이의 거리를 알 수 있음)
            print("%.1f"%distance)           # 거리값을 distance 변수에 입력하고 출력,  %.1f는 소수점 한자리 까지 출력
            time.sleep(1)
 
            RealTime += 1                    # RealTime라는 변수를 설정하고 ( 1초마다 동시에 realtime 변수도 시간을 같이 카운트)

            if (distance >= 20 and distance <= 50):     #  20< 거리 < 50 이면 사람이 있다고 판단 하고 count변수에 카운트 시작
                count += 1

            if (count == 10):                           # 바로 위에 count가 10이 되면 if문 실행, 초단위로 카운트를 입력하는 거리서 count = 10 도 거의 10초 쯤임
                print("start")                          # 여기 if문이 사람이 있는 것을 확인 했을 순간이니까, 여기 if문 안에 프로그래밍 하면됨
                GPIO.output(SENSER_OFF,False)           # led 빨간색을 off 하고
                GPIO.output(SENSER_ON,True)             # led 초록색을 on 한다

                RealTime = 0                     # 위에서 카운트한 realtime을 초기화 하고 다시 (사람이 왔을때의 시간)을 카운트 시작
                #if (RealTIme == 0)
                    
            if ( distance >= 100 ):              # 거리가 100 이상일 때, 시간을 err_time에 넣는다.
                ERR_TIME_1 = time.time()
                 
                ERR_ARRDIS.append(distance)      # ERR_ARRDIS 라는 리스트를 만들어서 100 이상이 되는 값을 리스트에 담는다. 
                i +=1                            # 추후 위 리스트를 가지고 (얼마의 시간동안 리스트가 10개 이상 찬다고 하면 사용자가 떠난 상황 이라고 생각 ) 말로 설명해줄께
            if i == 10:
                for j in range(10):              #ERR_ARRDIS 10개가 되면 리스트를 출력한다. (여기다가 TIME을 사용해서 프로그래밍, 튀는값 예외처리 부분)
                    print(ERR_ARRDIS[j])
             
        
    except KeyboardInterrupt:
        print("stopped by User")
        GPIO.cleanup()
