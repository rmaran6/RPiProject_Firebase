#LOG.py used to log diagnostic data
from datetime import datetime

def log(a): #Write string (a) to log file /home/pi/multithread-"date".log
    f=open("/home/pi/multithread-"+datetime.now().strftime("%d_%a_%b_%Y")+".log", "a+")
    f.write(str(datetime.now().strftime("%Y-%m-%d--%H:%M:%S"))+","+str(a)+"\n")
    f.close()

def log2(a): #Write string (a) to log file /home/pi/PIR-"date".log
    f=open("/home/pi/PIR-"+datetime.now().strftime("%d_%a_%b_%Y")+".log", "a+")
    f.write(str(datetime.now().strftime("%Y-%m-%d--%H:%M:%S"))+","+str(a)+"\n")
    f.close()

def log3(a): #Write string (a) to log file /home/pi/MW-"date".log
    f=open("/home/pi/MW-"+datetime.now().strftime("%d_%a_%b_%Y")+".log", "a+")
    f.write(str(datetime.now().strftime("%Y-%m-%d--%H:%M:%S.%f"))+","+str(a)+"\n")
    f.close()

def log4(a): #Write string (a) to log file /home/pi/BIST-"date".log
    f=open("/home/pi/BIST-"+datetime.now().strftime("%d_%a_%b_%Y")+".log", "a+")
    f.write(str(datetime.now().strftime("%Y-%m-%d--%H:%M:%S.%f"))+","+str(a)+"\n")
    f.close()
