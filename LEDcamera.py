import picamera
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)
time.sleep(0.1)
camera = picamera.PiCamera()
camera.capture('examaple.jpg')
time.sleep(0.1)
GPIO.output(18,GPIO.LOW)


GPIO.cleanup()
