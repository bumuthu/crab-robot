import picamera
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

try:
    while True:  
        GPIO.setup(18,GPIO.OUT)
        GPIO.output(18,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18,GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()

    
    
