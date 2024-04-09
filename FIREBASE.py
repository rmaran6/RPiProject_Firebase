#FIREBASE.py is used to communicate with the cloud database and upload/download files to cloud storage
import requests
import time
import LOG
import MAC
import firebase_admin
from firebase_admin import credentials
from google.cloud import storage

#Authenticate Firebase from json file on Desktop
params = ('auth', '/home/pi/authentication.json')
D_MAC = MAC.D_MAC #Get mac address of the ESP32
UPL_TO = 90 #Upload timeout in s

SET_URL = ''
GET_URL = ''
COMMAND_URL = ''
GET_USERID = ''
USERID_URL = ''
ACK_URL = ''
ALARM_URL = ''
PHONE_URL = ''
BUCKET_URL = ''


#Set user data on Firebase
def Set(F_USERID,child,value):
    global params
    print("SET: " + str(child) + ":" + str(value))
    LOG.log("SET: " + str(child) + ":" + str(value))
    data = '{\"'+child+'\":\"' +value+ '\"}'
    url=SET_URL
    while True:
        try:
            response = requests.patch(url, params=params, data=data, timeout=3)
            break
        except Exception as err:
            LOG.log(str(err))

#Get user data from Firebase
def Get(F_USERID,child):
    global params
    response = ""
    print("GET: " + str(child))
    LOG.log("GET: " + str(child))
    while True:
        try:
            response = (requests.get(GET_URL, params=params,timeout=3)).content
            return response.decode("utf-8").strip('\"')
        except requests.exceptions.ConnectionError as err: #If unable to pull data, log exceptions
            print("GET ERROR")
            LOG.log("GET ERROR")
            time.sleep(3)
        except requests.exceptions.RequestException as err:
            print("GET ERROR")
            LOG.log("GET ERROR")
            time.sleep(3)

#After App sets the "command" entry, this resets it to blank
def Reset_Command():
    global params,D_MAC
    data = '{\"command\":\"\"}'
    url=COMMAND_URL
    while True:
        try:
            response = requests.patch(url, params=params, data=data)
            break
        except Exception as e:
            LOG.log(str(e))

#Pull UserID from Firebase
def Get_USERID():
    global params,D_MAC
    while True:
        try:
            return requests.get(USERID_URL, params=params,timeout=10).content.decode("utf-8").strip('\"')
        except Exception as e:
            print(e)

#ACK that the video was uploaded
def Set_ACK(F_USERID,F_FILENAME):
    global params
    data='{\"filename\":\"'+F_FILENAME+'\"}'
    url=ACK_URL
    while True:
        try:
            response = requests.post(url, params=params, data=data)
            break
        except Exception as e:
            LOG.log(str(e))

#Log the time/location of the alarm
def Log_ALARM(F_USERID,F_FILENAME,D_POSITION):
    global params
    url=ALARM_URL
    data='{\"time\":\"'+F_FILENAME+'\",\"GPS\":\"'+D_POSITION+'\",\"acknowledged\":\"false\"}'
    while True:
        try:
            response = requests.post(url, params=params, data=data)
            break
        except Exception as e:
            LOG.log(str(e))

#Create a new Firebase Entry for new devices.
def Create_FB_Entry():
    global params,D_MAC
    url=PHONE_URL
    data = '{ "command": "","tile":"","uid":"unassigned"}'
    while True:
        try:
            response = requests.put(url, params=params, data=data)
            break
        except Exception as e:
            LOG.log(str(e))

#Upload file from D_PATH to Firebase path F_PATH
def Upload(F_PATH,D_PATH):
    global UPL_TO
    bucket = storage_client.get_bucket(BUCKET_URL) #Opens blob bucket to upload data
    blob = bucket.blob(F_PATH)
    blob.upload_from_filename(D_PATH,timeout=UPL_TO)
