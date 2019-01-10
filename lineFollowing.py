import RPi.GPIO as GPIO
import time
import multiprocessing
import picamera

GPIO.setmode(GPIO.BCM)

sensors = [27, 9, 5, 10, 6, 13, 26, 19]
count=0
for pin in range(8):
    GPIO.setup(sensors[pin],GPIO.IN)
while True:
    strg = ''
    val = []
    for pin in sensors:
        val.append(not (GPIO.input(pin)))
    
    print(val)
    time.sleep(0.1)
        
    

    

GPIO.cleanup()