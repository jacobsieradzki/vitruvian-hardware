#adapted from seeed wiki for grove slide potentiometer

import math
import sys
import time
#analogue to digital converter
from grove.adc import ADC
from multiprocessing import Process
import cv2
import os

#has a specific channel and can read adc value from it
class GroveFlex(ADC):
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def value(self):
        return self.adc.read(self.channel)

Grove = GroveFlex

def calibrate(s1,s2,t,n):
    n1s = []
    n2s = []
    i = 0
    while(i < t):
	n1s.append(s1.value)
	n2s.append(s2.value)
	i += 0.25
	time.sleep(0.25)
    n.append(sum(n1s)/len(n1s))
    n.append(sum(n2s)/len(n2s))
    print "calibration complete, n1: {}, n2: {}".format(n[0],n[1])


def main():
    #data reading
    sensor1 = GroveFlex(0)
    sensor2 = GroveFlex(2)
    ctime = 6
    norms = []
    threshold = 90
    calibrate(sensor1, sensor2, ctime, norms)


    timer = 0
    with open("poor_test_flex.txt", "w") as f:
        while True:
	    fl1 = sensor1.value
	    fl2 = sensor2.value
	    if (timer % 1 == 0):
            	print 'time: {} Flex sensor 1 VD value: {}mV'.format(str(timer), str(fl1))
            	print 'time: {} Flex sensor 2 VD value: {}mV'.format(str(timer), str(fl2))
            f.write('time: {} FS 1 VD: {}mV\n'.format(str(timer), str(fl1)))
	    f.write('time: {} FS 2 VD: {}mV\n'.format(str(timer), str(fl2)))
	    if (abs(fl1 - norms[0]) > threshold) :
	        os.system("python3 anglebuzz.py")
    	        print "******curve on flex sensor 1 detected****** \n"
                f.write("******curve on flex sensor 1 detected****** \n")
	    if (abs(fl2 - norms[1]) > threshold) :
	        os.system("python3 bendpulse.py")
	        print "******curve on flex sensor 2 detected****** \n"
                f.write("******curve on flex sensor 2 detected****** \n")
	    timer += 0.25
	    time.sleep(.25)



if __name__ == '__main__':
    main()
