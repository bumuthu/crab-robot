import RPi.GPIO as GPIO
import time
import multiprocessing
import numpy as np



GPIO.setmode(GPIO.BCM)

def rotServo(pin,angle):
    try: 
        p = GPIO.PWM(pin,50)
        p.start(10)
        duty = (angle/20.0)+3
        p.ChangeDutyCycle(duty)
        time.sleep(speedDelay)
        p.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()
    
def circleDetect():
    s1 = GPIO.input(24)
    s2 = GPIO.input(23)
    if(not(s1 or s2)):
        readyPhoto()
        capturePhoto()
        
def move(delta):
    global motor
    global possition1
    t7 = multiprocessing.Process(target=rotServo, args=(motor[6],possition1[6]+delta[6]))
    t1 = multiprocessing.Process(target=rotServo, args=(motor[0],possition1[0]+delta[0]))
    t2 = multiprocessing.Process(target=rotServo, args=(motor[1],possition1[1]+delta[1]))
    t3 = multiprocessing.Process(target=rotServo, args=(motor[2],possition1[2]+delta[2]))
    t4 = multiprocessing.Process(target=rotServo, args=(motor[3],possition1[3]+delta[3]))
    t5 = multiprocessing.Process(target=rotServo, args=(motor[4],possition1[4]+delta[4]))
    t6 = multiprocessing.Process(target=rotServo, args=(motor[5],possition1[5]+delta[5]))    
    t8 = multiprocessing.Process(target=rotServo, args=(motor[7],possition1[7]+delta[7]))
    
    t7.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    
    t8.start()
    
    t7.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join() 
    t5.join()
    t6.join()
    
    t8.join()
    
    
    
def ahead():
    
    l = lineFollow()
    a = l[0]+2
    b = l[1]+12
    c = l[2]
    d = l[3]
    e = l[4]
    move([0,-b,0,e,0,0,0,0])     
    move([0,-b,0,e,c,0,c-5,0])     
    move([-a,0,d+5,-10,c,0,c-5,0])
    #move([-a,0,d+5,-20,c,0,0,0]) 
    print(a,b,d,e,c)
    
    l = lineFollow()
    a = l[0]+2
    b = l[1]+12
    c = l[2]
    d = l[3]
    e = l[4]
    move([-a,0,d+5,-10,0,0,0,0])     
    move([-a,0,d+5,-10,0,-c+5,0,-c])     
    move([0,-b,0,e,0,-c+5,0,-c])
    #move([0,-b,0,e,0,0,0,-c]) 
    print(a,b,d,e,c)
    
    
    
def aheadNotTurn():
    a,b,d,e,c = 45,45,50,50,30
    move([0,-b,0,e,0,0,0,0])     
    move([0,-b,0,e,c,0,c-5,0])     
    move([-a,0,d+5,-10,c,0,c-5,0])
    move([-a,0,d+5,-10,0,0,0,0])     
    move([-a,0,d+5,-10,0,-c+5,0,-c])     
    move([0,-b,0,e,0,-c+5,0,-c])
  
    
def reverse():
    a, b, d, e, c = 40, 40, 40, 40, 30

    
    move([a,0,-d,0,c,0,c,0]) 
    move([a,0,-d,0,0,0,0,0])
    move([a,0,-d,0,0,-c,0,-c-10])
    #move([a,0,-d,0,0,-c,0,-c-10])
    move([0,b,0,-e,0,-c,0,-c-10]) 
    move([0,b,0,-e,0,0,0,0])
    '''
    move([0,b,0,-e,c,0,c,0]) 
    move([a,b,d,-e,c,0,c,0]) 
    move([a,b,d,-e,0,0,0,0]) '''
       
    

       
    
def leftTurn():
    a, b, d, e, c = 20, 20, 20, 20, 30
    
    move([0,0,0,0,0,-c,0,-c]) 
    move([a,-b,d,-e,0,-c,0,-c]) 
    move([a,-b,d,-e,0,0,0,0]) 
    move([-a,b,-d,e,c,0,c,0]) 
    move([-a,b,-d,e,0,0,0,0]) 
    
def rightTurn():    
    a, b, d, e, c = 28, 28, 28, 28, 30
    
    move([0,0,0,0,c,0,c,0]) 
    move([a,0,d,0,c,0,c,0]) 
    move([a,0,d,0,0,0,0,0]) 
    move([-a,0,-d,0,0,-c,0,-c]) 
    move([-a,b,-d,e,0,0,0,0]) 
    
def readyPhoto():
    move([50,-50,50,-50,0,0,0,0])
    
def capturePhoto():
    global imCount
    global camera
    imCount+=1
    #GPIO.output(18,GPIO.HIGH)
    time.sleep(0.1)
    
    camera.capture('arrow.jpg')
    time.sleep(0.1)
    #GPIO.output(18,GPIO.LOW)
    
    

def imageProcessing():
    global brightnessThreshold 

    img0 = cv.imread('arrow.jpg', cv.IMREAD_GRAYSCALE)
    ret, thresh = cv.threshold(img0, brightnessThreshold, 255, 0)
    x1, y1, x2, y2 = 200, 500, 500, 800
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv.erode(thresh, kernel, iterations=5)
    filtered = cv.bilateralFilter(erosion, 10, 1000, 1000)
    img = filtered  # [x1:y1, x2:y2]
    corners = cv.goodFeaturesToTrack(img, 3, 0.01, 10)
    imgc = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    try:
        for corner in corners:
            x, y = corner.ravel()
            cv.circle(imgc, (x, y), 5, 255, -1)
        coord = corners.ravel()
        #print(coord)
        distList = []
        for i in range(0, 5, 2):
            x, y = coord[i], coord[i + 1]
            dist = 0
            for j in range(0, 5, 2):
                if j != i:
                    a, b = coord[j], coord[j + 1]
                    dist += (x - a) * (x - a) + (y - b) * (y - b)
            distList.append(dist)
        #print(distList)

        frontX, frontY = coord[2 * distList.index(max(distList))], coord[2 * distList.index(max(distList)) + 1]
        backPoints = []
        for i in range(0, 5, 2):
            if i != 2 * distList.index(max(distList)):
                backPoints.append(coord[i])
                backPoints.append(coord[i + 1])

        midX = (backPoints[0] + backPoints[2]) / 2
        deltaX = frontX - midX
        cv.imwrite('processedImage.jpg',imgc)
        print(abs(deltaX) )
        if abs(deltaX) < 40:
            print("ahead")
            aheadNotTurn()
            aheadNotTurn()
            aheadNotTurn()
            aheadNotTurn()
            aheadNotTurn()
                  

        elif deltaX > 0:
            print("right")
            aheadNotTurn()
            aheadNotTurn()
            rightTurn()
            rightTurn()
            rightTurn()
        
            aheadNotTurn()
            aheadNotTurn()
            aheadNotTurn()
                   

        elif deltaX < 0:
            print("left")
            aheadNotTurn()
            aheadNotTurn()
            leftTurn()
            leftTurn()
            
            aheadNotTurn()
            aheadNotTurn()
            aheadNotTurn()
            
    except TypeError:
        print('stop')
        aheadNotTurn()
        aheadNotTurn()
        aheadNotTurn()
        readyPhoto()
        time.sleep(20)
               
    
def lineFollow():
    global kp, kd, prerror, sensors
    s = []
    for pin in sensors:
        s.append(int(not(GPIO.input(pin))))        
          
    if (not (s[0] or s[1] or s[2] or s[3] or s[4] or s[5] or s[6] or s[7] or s[8] or s[9])):
        error = prerror
    elif (s[0] and not(s[1] or s[2] or s[3] or s[4] or s[5] or s[6] or s[7])):
        error = -35
    elif (s[7] and not(s[1] or s[2] or s[3] or s[4] or s[5] or s[6] or s[0])):
        error = 40
    elif ((s[0] and s[1]) and (not(s[2] or s[3] or s[4] or s[5] or s[6] or s[7]))):
        error = -25
    elif ((s[7] and s[6]) and (not(s[1] or s[2] or s[3] or s[4] or s[5] or s[0]))):
        error = 30           
    else:
        error = (s[0]*(-5)+s[1]*(-3)+s[2]*(-2)+s[3]*0+s[4]*0+s[5]*2+s[6]*3+s[7]*5)*20.0/10.0
            
    PD = kp*error           
    turn = PD
    print(turn)
    
    f = 40.0
    c = 30.0
    
    if turn>=0:
        a = f-turn  
        b = f-turn
        d = f
        e = f
    else:
        a = f
        b = f
        d = f+turn-20 
        e = f+turn-20

    prerror = error    
    return (a,b,c,d,e)

motor = [21,2,3,16,12,4,22,20]
possition1 = [80, 105, 75, 90, 95, 95, 65-5, 110]
for pin in motor:    
    GPIO.setup(pin,GPIO.OUT)
sensors = [8, 9, 5, 10, 6, 13, 26, 19, 24, 23]
for pin in sensors:
    GPIO.setup(pin,GPIO.IN)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(11,GPIO.IN)
indicator1 = 25
#indicator2 
indicator3 = 7
GPIO.setup(indicator1,GPIO.OUT)
#GPIO.setup(indicator2,GPIO.OUT)
GPIO.setup(indicator3,GPIO.OUT)
GPIO.setup(18,GPIO.OUT) 
camera = picamera.PiCamera()
sleepTime = 0

brightnessThreshold = 130     #black up when value up
#brightnessThrehold = 150
imCount = 0
prerror = 0
kp = 1.4

speedDelay = 0.2

#move([0,0,0,0,0,0,0,0])
time.sleep(1)
try:    
    while True:
        
        codeRunningKey = GPIO.input(11)
        move([0,0,0,0,0,0,0,0,])
        aheadNotTurn()
        aheadNotTurn()
        aheadNotTurn()
    
        
        while codeRunningKey:
            codeRunningKey = GPIO.input(11)
            print('running')
            
            ahead()
            
            
           
            
       
        while not(codeRunningKey):            
            codeRunningKey = GPIO.input(11)
            time.sleep(0.5)
            print('not running')
         
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()



