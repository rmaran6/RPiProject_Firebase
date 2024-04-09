#Main multithreaded program

import socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 9999))

import signal, os, coverage
cov = coverage.Coverage()
cov.start()

def handler(signum, frame):
    cov.save()

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGUSR1, handler)

import LED #Import libraries
LED.BLUE() #Blue LEDs for initialization
import LOG
LOG.log('\n\n\n====================BOOTUP=====================')
import threading
import time
import os
import MAC
import FIREBASE
import BUZZER
import SENSOR
import CAMERA
import BIST
import serial
import json
from firebase_admin import db
from datetime import datetime

#DELAYS for each thread
T1_D = .1
T2_D = 1
T3_D = .2
T5_D = .4

#DEVICE Flags
D_MAC = MAC.D_MAC #MAC of the pi
D_MODE = 'ARMED' #Current device mode
D_FILENAME = "" #Filename of recorded video
D_PIR = 0
D_VIDEOPATH = CAMERA.D_VIDEOPATH #Folder for video files, json files
D_BUTTON = False
D_RECORDING = False #Is the device recording
MOT_ARR = '' #Array containing motion data for the video

#FIREBASE Flags
F_ALARM = 'false' #Firebase flag for alarm
F_ARMED = 'true' #Firebase flag for armed
F_FILENAME = "" #Filename of uploaded video
F_USERID = FIREBASE.Get_USERID() #Pull User ID from Firebase
print(F_USERID)

#Globals
ALARM_TIMEOUT = 60 #Alarm timeout
ARMED_MAX_RECORDTIME = 20 #Video starts recording on Chirp. If alarm is never triggered, it will record for this amount of time and then delete the video.

def stream_handler(message): #Creates web socket that listens to the 'COMMAND' bit on Firebase for commands from mobile app
    global D_MODE,D_BUTTON
    A = str(message.data) #Read 'COMMAND' bit from FIrebase
    LOG.log('Web Socket Reading: ' + A)
    if (A == 'reboot'): #Reboots Device
        FIREBASE.Reset_Command()
        D_MODE = 'REBOOT'
        time.sleep(1)
        LED.LED_OFF()
        os.system('sudo reboot')
    if (A == 'alarm_off'): #Turn off Alarm
        D_BUTTON = True
        if D_MODE == 'ALARM':
            LOG.log('Disarmed from Mobile')
            D_MODE = 'UPLOADING'
        if D_MODE == 'ALARM_UPLOADED':
            LOG.log('Disarmed from Mobile, post upload')
            D_MODE = 'ARMED'
        FIREBASE.Reset_Command()
    if (A == 'BIST'): #Built-in-self-test
        FIREBASE.Reset_Command()
        if D_MODE == 'ARMED':
            D_MODE = 'BIST'
            BIST.BIST()
            time.sleep(1)
            D_MODE = 'ARMED'
dbref = db.reference('phone_lookup/' + D_MAC + '/command').listen(stream_handler) #Start web socket

def init(): #Initialization thread: starts web socket and  pulls user data,
    FIREBASE.Set(F_USERID,'alarm','false')
    FIREBASE.Set(F_USERID,'armed','true')
    FIREBASE.Set(F_USERID,'mode','normal')
    LOG.log(str(F_USERID))
    LOG.log("Done Initializing")

def thread1(): #Handles logic between sensors,states,etc
    global F_USERID,D_MODE,T1_D,D_FILENAME,ARMED_MAX_RECORDTIME,D_VIDEOPATH,ALARM_TIMEOUT,F_FILENAME,D_PIR,MOT_ARR,D_BUTTON,D_RECORDING
    record_start = 0 #Stores the start time of the video
    MOT_ARR = '' #Array containing motion data for the video
    while True:
        P1 = SENSOR.SENS1() #Sensor1 val
        P2 = SENSOR.SENS2() #Sensor2 val
        if (P1 or P2):
            D_PIR = 1
        else:
            D_PIR = 0
        if (D_MODE == 'ARMED'): #Armed state
            D_BUTTON = False
            if D_RECORDING:
                curr_time = time.time()
                if (curr_time - record_start) > ARMED_MAX_RECORDTIME: #Stop recording after a minute of recording in 'ARMED'
                    CAMERA.stop_recording()
                    D_RECORDING = False
                    os.system('sudo rm ' + D_VIDEOPATH + D_FILENAME + '.h264') #Delete recorded file
                    MOT_ARR = ''
            if D_PIR:
                LOG.log('ALARM')
                print('ALARM')
                alarm_start = time.time() #Start time of the alarm
                D_MODE = 'ALARM'
                if not D_RECORDING: #If recording hasnt started, start it here. This should ideally never occur
                    record_start = time.time()
                    F_FILENAME=str(datetime.now())[:-7] + time.tzname[0] #Video filename is date and timezone
                    D_FILENAME = 'test' + datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d--%H-%M-%S')
                    LOG.log('Taking thumbnail')
                    CAMERA.thumbnail()
                    LOG.log('Uploading thumbnail')
                    FIREBASE.Upload(F_USERID+'/thumbnail.jpg',D_VIDEOPATH + 'thumbnail.jpg')
                    LOG.log('Thumbnail Uploaded')
                    CAMERA.start_recording(D_FILENAME,ALARM_TIMEOUT) #Start recording
                    D_RECORDING = True

        elif (D_MODE == 'ALARM'): #Alarm  state
            curr_time = time.time()
            if (curr_time - record_start) > ARMED_MAX_RECORDTIME:
                D_MODE = 'UPLOADING'

        elif (D_MODE == 'ALARM_UPLOADED'): #Alarm is uploaded, waiting for timeout or button_press
            if D_BUTTON:
                D_MODE = 'ARMED'
                D_BUTTON = False
            curr_time = time.time()
            if (curr_time - alarm_start) > ALARM_TIMEOUT: #Timeout alarm after ALARM_TIMEOUT
                LOG.log("ALARM timed out")
                D_MODE = 'ARMED'

        elif (D_MODE == 'UPLOADING'): #Uploading state
            CAMERA.stop_recording() #Stop recording
            D_RECORDING = False
            time.sleep(.1)
            CAMERA.convert_mp4(D_FILENAME)
            D_JS = {'sensorData':{'motion':MOT_ARR[:-1]},'offset':0} #Put MOT_ARR in json format
            json.dump(D_JS,open(D_VIDEOPATH + D_FILENAME + '.json','w')) #Dump json file for upload
            MOT_ARR = ''
            LOG.log("Starting Upload")
            FIREBASE.Upload(F_USERID+'/'+F_FILENAME+ '.json',D_VIDEOPATH + D_FILENAME + '.json') #upload json file
            FIREBASE.Upload(F_USERID+'/'+F_FILENAME+ '.mp4',D_VIDEOPATH + D_FILENAME + '.mp4') #upload video file
            print("Done Uploading" + str(F_FILENAME))
            LOG.log("Done Uploading: " + str(F_FILENAME))
            os.system('sudo rm ' + D_VIDEOPATH + D_FILENAME + '.mp4') #Delete mp4
            os.system('sudo rm ' + D_VIDEOPATH + D_FILENAME + '.h264') #Delete h264
            os.system('sudo rm ' + D_VIDEOPATH + D_FILENAME + '.json') #Delete json
            D_MODE = 'ALARM_UPLOADED'
        time.sleep(T1_D)

def thread2(): #Handles Firebase Flags
    global F_ALARM,F_ARMED,D_MODE,T2_D,F_USERID,F_FILENAME,D_RECORDING
    while True:
        if (D_MODE == 'ARMED') and ((F_ARMED == 'false') or (F_ALARM == 'true')): #If entering ARMED from UPLOADING or ALARM, update Firebase flags
            FIREBASE.Set(F_USERID,'armed', 'true') #update 'armed' and 'alarm' entries
            FIREBASE.Set(F_USERID,'alarm', 'false')
            F_ALARM = 'false'
            F_ARMED = 'true'
        if (D_MODE == 'ALARM') and (F_ALARM == 'false') and D_RECORDING: #If entering ALARM from ARMED, update Firebase flag
            FIREBASE.Set(F_USERID,'alarm', 'true') #update 'armed' and 'alarm' entries
            FIREBASE.Set(F_USERID,'armed', 'true')
            F_ALARM = 'true'
            F_ARMED = 'true'
            tz = time.tzname[0]
            dt = str(datetime.now()).replace(' ','|')[:-7] + tz
            D_POSITION = '3347.733822,N,08424.735922,W,080421,200651.0,333.8,0.0,0.0'
            FIREBASE.Log_ALARM(F_USERID,F_FILENAME,D_POSITION + '|' + dt) #Log the alarm with the time
            LOG.log('Alarm logged')
        time.sleep(T2_D)

def thread3(): #LED State Machine
    global D_MODE,T3_D
    Loop = 1
    while True:
        if D_MODE == 'ARMED':
            BUZZER.buzzer_off()
            LED.LED_OFF() #Off during armed
        elif D_MODE == 'ALARM' or D_MODE == 'UPLOADING' or D_MODE == 'ALARM_UPLOADED':
            BUZZER.buzzer_on()
            LED.ALARM_FLASH(Loop) #Flashing red and white when alarming and uploading
        if Loop == 12:
            Loop = 1
        else:
            Loop = Loop + 1
        time.sleep(T3_D)

def main(): #Start Threads
    init()
    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)
    t3 = threading.Thread(target=thread3)
    t1.start()
    t2.start()
    t3.start()
    t1.join()

main()
