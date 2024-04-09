import RPi.GPIO as GPIO
import time

BUZZ = 5
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZZ, GPIO.OUT)

def buzzer_on():
    GPIO.output(BUZZ, GPIO.HIGH)

def buzzer_off():
    GPIO.output(BUZZ, GPIO.LOW)

def buzzer_chirp(): #Chirping sequence
    buzzer_on()
    time.sleep(.2)
    buzzer_off()
    time.sleep(.1)
    buzzer_on()
    time.sleep(.3)
    buzzer_off()
