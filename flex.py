#adapted from seeed wiki for grove slide potentiometer

import math
import sys
import time
#analogue to digital converter
from grove.adc import ADC
from multiprocessing import Process
import cv2

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
    out = cv2.VideoWriter('mflex.avi',fourcc, 20.0, (640,480))


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
    webcam = Process(target = record)
    webcam.start()

    #error handling
    #if len(sys.argv) < 2:
    #    print('Usage: {} adc_channel'.format(sys.argv[0]))
    #    sys.exit(1)

    #data reading
    sensor1 = GroveFlex(0)
    sensor2 = GroveFlex(2)
    while True:
        print('Flex sensor 1 VD value: {}mV'.format(sensor1.value))
        print('Flex sensor 2 VD value: {}mV'.format(sensor2.value))
        time.sleep(.2)

    webcam.terminate()



if __name__ == '__main__':
    main()
