import RPi.GPIO as GPIO

P1 = 27
P2 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(P1, GPIO.IN)
GPIO.setup(P2, GPIO.IN)

def SENS1():
    return GPIO.input(P1)

def SENS2():
    return GPIO.input(P2)
