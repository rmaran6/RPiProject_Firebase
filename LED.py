#LED.py is used to communicate to the IS31FL3236A LED driver
import smbus
import time
import numpy as np
import RPi.GPIO as GPIO
SHUTDOWN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SHUTDOWN, GPIO.OUT)

BLINK_SPEED = 6 #Speed used during PWM blinking

try:
    bus = smbus.SMBus(1) #Initializes i2c bus1
except Exception as e:
    print("No Led-Driver Detected")
    pass

def bus_write(REG, VAL): #Writes VAL to i2c register REG at address 0x3C
    ADDR = 0x3C
    try:
        bus.write_byte_data(ADDR, REG, VAL)
    except Exception as e:
        print(e)
        pass

def upd_LED(): #Writes 0 to PWM Update Register. Updates LED status and PWM value
    bus_write(37,0x00)

def set_LED(r, br, g, bg, b, bb): #Takes 3 arrays for which LEDs and 3 arrays for the brightness of each LED in the array
    for x in range(1,13):
        if x in r:
            bus_write(35 + 3*x, 0x01) #Writes 0x01 if LED is to be turned on
            bus_write(3*x - 2, br[r.index(x)]) #Writes the corresponding brightness to the PWM register
        else:
            bus_write(35 + 3*x, 0) #Writes 0x00 if LED is to be turned off
            bus_write(3*x - 2, 0) #Writes 0 to the PWM register
        if x in g:
            bus_write(36 + 3*x, 0x01) #Same for Green
            bus_write(3*x - 1, bg[g.index(x)])
        else:
            bus_write(36 + 3*x, 0)
            bus_write(3*x - 1, 0)
        if x in b:
            bus_write(37 + 3*x, 0x01) #Same for Blue
            bus_write(3*x, bb[b.index(x)])
        else:
            bus_write(37 + 3*x, 0)
            bus_write(3*x, 0)
    upd_LED()

def LED_OFF(): #Turns off all LEDs
    set_LED([],[],[],[],[],[])

def RED(): #Turn on all Red LEDs at max brightness
    set_LED([1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255],[],[],[],[])

def BLUE(): #Turn on all Green LEDs at max brightness
    set_LED([],[],[1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255],[],[])

def GREEN(): #Turn on all Blue LEDs at max brightness
    set_LED([],[],[],[],[1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255])

def YELLOW(): #Turn on all Red and Green LEDs at max brightness
    set_LED([1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255],[1,2,3,4,5,6,7,8,9,10,11,12],[100,100,100,100,100,100,100,100,100,100,100,100],[],[])

def CYAN(): #Turn on all Green and Blue LEDs at max brightness
    set_LED([],[],[1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255],[1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255])

def PURPLE(): #Turn on all Red and Blue LEDs at max brightness
    set_LED([1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255],[],[],[1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255])

def WHITE(): #Turn on all 36 LEDs at max brightness
    set_LED([1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255],[1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255],[1,2,3,4,5,6,7,8,9,10,11,12],[255,255,255,255,255,255,255,255,255,255,255,255])

def RED_Loop(x,LOOP_SPEED,L): #x is the starting LED for the loop, L is the length of the loop, LOOP_SPEED is the delay between segments of the loop
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)):
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    arr2 = [255] * len(arr)
    set_LED(arr,arr2,[],[],[],[])
    time.sleep(LOOP_SPEED)

def GREEN_Loop(x,LOOP_SPEED,L): #Same for green
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)):
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    arr2 = [255] * len(arr)
    set_LED([],[],arr,arr2,[],[])
    time.sleep(LOOP_SPEED)

def BLUE_Loop(x,LOOP_SPEED,L): #Same for blue
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)):
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    arr2 = [255] * len(arr)
    set_LED([],[],[],[],arr,arr2)
    time.sleep(LOOP_SPEED)

def RED_Loop2(x,LOOP_SPEED,L): #x is the starting LED for the loop, L is the length of the loop, LOOP_SPEED is the delay between segments
    if x == 2: #Reverses direction of loop from RED_Loop(). Both functions can take a 1-12 input
        x = 12
    elif x == 3:
        x = 11
    elif x == 4:
        x = 10
    elif x == 5:
        x = 9
    elif x == 6:
        x = 8
    elif x == 8:
        x = 6
    elif x == 9:
        x = 5
    elif x == 10:
        x = 4
    elif x == 11:
        x = 3
    elif x == 12:
        x = 2
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)): #Loop from 1-12
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    #arr2 = [255] * len(arr)
    arr2 = [255] * (len(arr) - 2) + [130] + [50]
    set_LED(arr,arr2,[],[],[],[])
    time.sleep(LOOP_SPEED)

def GREEN_Loop2(x,LOOP_SPEED,L): #Same for green
    if x == 2: #Reverses direction of the Loop
        x = 12
    elif x == 3:
        x = 11
    elif x == 4:
        x = 10
    elif x == 5:
        x = 9
    elif x == 6:
        x = 8
    elif x == 8:
        x = 6
    elif x == 9:
        x = 5
    elif x == 10:
        x = 4
    elif x == 11:
        x = 3
    elif x == 12:
        x = 2
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)): #Loop from 1-12
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    #arr2 = [255] * len(arr)
    arr2 = [255] * (len(arr) - 2) + [120,50]
    set_LED([],[],arr,arr2,[],[])
    time.sleep(LOOP_SPEED)

def BLUE_Loop2(x,LOOP_SPEED,L): #Same for blue
    if x == 2: #Reverses direction
        x = 12
    elif x == 3:
        x = 11
    elif x == 4:
        x = 10
    elif x == 5:
        x = 9
    elif x == 6:
        x = 8
    elif x == 8:
        x = 6
    elif x == 9:
        x = 5
    elif x == 10:
        x = 4
    elif x == 11:
        x = 3
    elif x == 12:
        x = 2
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)): #Loop from 1-12
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    arr2 = [255] * (len(arr)-2) + [100,40]
    set_LED([],[],[],[],arr,arr2)
    time.sleep(LOOP_SPEED)


def CYAN_Loop(x,LOOP_SPEED,L): #x is the starting LED for the loop, L is the length of the loop, LOOP_SPEED is the delay between segments of the loop
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)):
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    arr2 = [255] * len(arr)
    set_LED([],[],arr,arr2,arr,arr2)
    time.sleep(LOOP_SPEED)

def YELLOW_Loop(x,LOOP_SPEED,L): #Same for yellow
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)):
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    arr2 = [255] * len(arr)
    set_LED(arr,arr2,arr,arr2,[],[])
    time.sleep(LOOP_SPEED)

def PURPLE_Loop(x,LOOP_SPEED,L): #Same for purple
    arr = list(np.linspace(x,x+L-1,L))
    for temp in range(0,len(arr)):
        if arr[temp] > 12:
            arr[temp] = arr[temp] - 12
    arr2 = [255] * len(arr)
    set_LED(arr,arr2,[],[],arr,arr2)
    time.sleep(LOOP_SPEED)

def RED_Blink(): #Fades LEDs from max brightness to 0 and back to max brightness. Speed of the fade depends on BLINK_SPEED
    global BLINK_SPEED
    RED()
    for i in range(255,-1,-1*BLINK_SPEED):
        for j in range(1,37):
            bus_write(j,i)
        upd_LED()
    for i in range(0,256,BLINK_SPEED):
        for j in range(1,37):
            bus_write(j,i)
        upd_LED()

def GREEN_Blink(): #Same for green
    global BLINK_SPEED
    GREEN()
    for i in range(255,-1,-1*BLINK_SPEED):
        for j in range(1,37):
            bus_write(j,i)
        upd_LED()
    for i in range(0,256,BLINK_SPEED):
        for j in range(1,37):
            bus_write(j,i)
        upd_LED()

def BLUE_Blink(): #Same for blue
    global BLINK_SPEED
    BLUE()
    for i in range(255,-1,-1*BLINK_SPEED):
        for j in range(1,37):
            bus_write(j,i)
        upd_LED()
    for i in range(0,256,BLINK_SPEED):
        for j in range(1,37):
            bus_write(j,i)
        upd_LED()

def ALARM_FLASH(x): #Flahes red and off. Used for an alarm
    if x % 2 == 0:
        RED()
    elif x % 2 == 1:
        LED_OFF()
        #WHITE()

GPIO.output(SHUTDOWN, GPIO.HIGH)
bus_write(0x25,0x00) #Set update register to 0
bus_write(0x4B,0x01) #Set output frequency to 22kHz
bus_write(0x00,0x01) #Set shutdown register to normal operation
