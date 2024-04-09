# ADC.py is used to read from the 4-channel ADC on i2c bus-1 and i2c address 0x49
import io
import fcntl
import time
import math
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115(address=0x49,busnum=0) #16 Bit ADC on i2c bus 1 at i2c address 0x49
adc.mode = 1 #Sets mode to continous, allowing faster reading
REF_V = 6.144 #Set gain to 2/3, allows readings from -6.1V to 6.1V

#Read from the 4 Channels of the ADC at 0x49
def CH0(): #Return voltage from channel 0
    global REF_V
    try:
        CH0_V = (adc.read_adc(0,gain=2/3) / 32768) * REF_V #Read voltage
        return CH0_V
    except Exception as e:
        print("Cant read channel 0",e)
        return 0

def CH1(): #Return voltage from channel 1
    global REF_V
    try:
        CH1_V = (adc.read_adc(1,gain=2/3) / 32768) * REF_V
        return CH1_V
    except Exception as e:
        print("Cant read channel 1",e)
        return 0

def CH2(): #Return voltage from channel 2
    global REF_V
    try:
        CH2_V = (adc.read_adc(2,gain=2/3) / 32768) * REF_V
        return CH2_V
    except Exception as e:
        print("Cant read channel 2",e)
        return 0

def CH3(): #Return voltage from channel 3
    global REF_V
    try:
        CH3_V = (adc.read_adc(3,gain=2/3) / 32768) * REF_V
        return CH3_V
    except Exception as e:
        print("Cant read channel 3",e)
        return 0
