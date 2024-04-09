import os

D_VIDEOPATH = '/home/pi/Desktop/RPiProject_Firebase/Videos/'

def thumbnail():
    os.system('/home/pi/Desktop/RPiProject_Firebase/veye_raspistill -o ' + D_VIDEOPATH + 'thumbnail.jpg')

def start_recording(filename,duration):
    os.system('/home/pi/Desktop/RPiProject_Firebase/veye_raspivid -t ' + str(duration) + '000 -o ' + D_VIDEOPATH + filename + '.h264 &')

def stop_recording():
    PID_ARR = os.popen('pidof veye_raspivid').read().rstrip().split()
    for PID in PID_ARR:
        os.system('sudo kill ' + PID)

def convert_mp4(filename):
    os.system('MP4Box -add ' + D_VIDEOPATH + filename + '.h264 ' + D_VIDEOPATH + filename + '.mp4')
