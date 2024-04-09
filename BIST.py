# BIST.py is used for built-in self testing. Automatically runs BIST1-4 and prints pass/fail.
import os
import subprocess
import BUZZER
import time
import LOG

def BIST():
    #Ensure that every i2c device is detected
    NUM_FOUND = 0
    p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
    for i in range(0,9):
        try:
            line = str(p.stdout.readline())
            A = line.split(':')[1].rstrip()
            if ('3c' in A): # LED Driver
                NUM_FOUND = NUM_FOUND + 1
        except Exception as e:
            pass
    if (NUM_FOUND == 1):
        print(str(NUM_FOUND) + ' I2C Devices Found. BIST1 Test Passed') #LED Driver found
        import LED
        time.sleep(1) #Test all LED Colors
        LED.RED()
        time.sleep(1)
        LED.GREEN()
        time.sleep(1)
        LED.BLUE()
        time.sleep(1)
        LED.LED_OFF()
    else:
        print(str(NUM_FOUND) + ' I2C Devices Found. BIST1 Test Failed')

    #Read CPU temperature and ensure it is under 100°F
    f = open('/sys/class/thermal/thermal_zone0/temp','r')
    temp = f.readline().rstrip()
    temp = abs(int(temp)) / 1000
    if temp < 100:
        print('Temperature: ' + str(temp) + 'F. BIST2 Test Passed')
    else:
        print('Temperature: ' + str(temp) + 'F. BIST2 Test Failed')

    #Check for USB Connection
    dev_arr = os.listdir('/dev/')
    if 'ttyUSB0' in dev_arr:
        print('UART Found. BIST3 Test Passed')
    else:
        print('UART Not found. BIST3 Test Failed')

    #Record Video and Check for File Size
    os.system('/home/pi/Desktop/RPiProject_Firebase/veye_raspivid -t 5000 -o /dev/shm/BIST_test.h264')
    VID_SIZE = os.stat('/dev/shm/BIST_test.h264').st_size
    if VID_SIZE > 1000000:
        print('Valid Video Recorded. BIST5 Test Passed')
    else:
        print('Valid Video not Recorded. BIST5 Test Failed')
    os.system('sudo rm /dev/shm/BIST_test.h264')

    #Chirp the Buzzer once to test connection
    BUZZER.buzzer_chirp()
    time.sleep(1)

    #Run Speedtest-cli
    os.system('sudo speedtest-cli')

def Temp_I2C_Log():
    while True:
        #Ensure that every i2c device is detected
        NUM_FOUND = 0
        p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
        for i in range(0,9):
            try:
                line = str(p.stdout.readline())
                A = line.split(':')[1].rstrip()
                if ('3c' in A): # LED Driver
                    NUM_FOUND = NUM_FOUND + 1
            except Exception as e:
                pass
        if (NUM_FOUND == 1):
            LOG.log4("LED Driver Found")
        else:
            LOG.log4("LED Driver not Found")

        #Read CPU temperature and ensure it is under 100°F
        f = open('/sys/class/thermal/thermal_zone0/temp','r')
        temp = f.readline().rstrip()
        temp = abs(int(temp)) / 1000
        LOG.log4('Temperature: ' + str(temp))
        time.sleep(1)
