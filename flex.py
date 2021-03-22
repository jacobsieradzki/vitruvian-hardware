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

#recording function
def record():
    cap = cv2.VideoCapture("/dev/video1")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('flex.avi',fourcc, 20.0, (640,480))


    if (cap.isOpened() == False):
        print("Error reading video file")

    while cap.isOpened():
        #read the current frame
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.flip(frame,0)
            # write the flipped frame
            out.write(frame)
            #show said frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


Grove = GroveFlex


def main():

    #multiprocessing management
    #webcam = Process(target = record)
    #webcam.start()

    #error handling
    #if len(sys.argv) < 2:
    #    print('Usage: {} adc_channel'.format(sys.argv[0]))
    #    sys.exit(1)

    #data reading
    sensor1 = GroveFlex(0)
    sensor2 = GroveFlex(2)

    ctime = 0
    n1s = []
    n2s = []
    while(ctime < 6):
	n1s.append(sensor1.value)
	n2s.append(sensor2.value)
	ctime += 0.25
	time.sleep(0.25)    
    norm1 = sum(n1s)/len(n1s)
    norm2 = sum(n2s)/len(n2s)
    print "calibration complete, n1: {}, n2: {}".format(norm1,norm2)

    timer = 0
    with open("test_flex.txt", "w") as f:
        while True:
	    fl1 = sensor1.value
	    fl2 = sensor2.value
	    if (timer % 1 == 0):
                print('time: {} Flex sensor 1 VD value: {}mV'.format(str(timer), str(fl1)))
                print('time: {} Flex sensor 2 VD value: {}mV'.format(str(timer), str(fl2)))
            f.write('time: {} FS 1 VD: {}mV\n'.format(str(timer), str(fl1)))
	    f.write('time: {} FS 2 VD: {}mV\n'.format(str(timer), str(fl2)))
	    if (abs(fl1 - norm1) > 100) :
		os.system("python3 anglebuzz.py")
		print "flex sensor 1 detected"
	    if (abs(fl2 - norm2) > 100) :
		os.system("python3 bendpulse.py")
		print "flex sensor 2 detected"
	    timer += 0.25
	    time.sleep(.25)

    #webcam.terminate()



if __name__ == '__main__':
    main()
