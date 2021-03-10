from picamera import PiCamera
import time
import sys
import FaBo9Axis_MPU9250 as MPU
from datetime import datetime
import math
import smbus
import cv2
from multiprocessing import Process

#setup filepath (using time of recording)
now = datetime.now()
current_time = now.strftime("%H_%M_%S")
filepath = "Documents/TestingOutput/"

#selects the first device on the mux by default
bus = smbus.SMBus(1)
dev = [0b00000001, 0b00000010]
addr = 0x70
bus.write_byte(addr,dev[0])
mpu = MPU.MPU9250()


##check if string can be converted to int
#def RepresentInt(str):
    #try:
        #int(str)
	#return True
    #except ValueError:
	   #return False

#recording function
def record():
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

# Calibrate a "normal" value (taking the average from cal_length samples).
def calibrate(cal_length) :
    norm = 0
    i = 0
    cal_angles = []
    while i < cal_length:
        theta = []
        print(i)
        #loop for both devices, add the appropriate values to the recorded values
        for j in dev:
            bus.write_byte(addr,j)
            accel = mpu.readAccel()
            y = accel['y'] + 0.00000001
            z = accel['z'] + 0.00000001
            theta.append(math.degrees(math.atan(y/z)))
        angle = sum(theta)/len(theta)
        #get the average angle of the sensors
        cal_angles.append(angle)
        time.sleep(0.25)
    	i+=0.25

    #get the average over all readings
    norm = sum(cal_angles)/len(cal_angles)
    print "Normal angle set to: " + str(norm)
    print "\n"
    return norm


def dataloop():
    #get the normal over 4 data inputs
    normal = calibrate(4)

    #data poll loop
    #input "poll" to retrieve current sensor data
    #input "calibrate" to recalibrate the normal
    #input "quit" to exit to exit data poll loop
    while True:


        input = raw_input()
        #data poll command
        if input == "poll":
            angle = 0
            curve = 0
            theta = []
            #loop through IMUs and calculate angle of each
            for j in dev:
                bus.write_byte(addr, j)
                accel = mpu.readAccel()
                y = accel['y'] + 0.00000001
                z = accel['z'] + 0.00000001
                theta.append(math.degrees(math.atan(y/z)))
            #calculate average back angle and curve
            angle = sum(theta)/len(theta)
            curve = theta[0] - theta[1]
            print "Back angle: " + str(angle) + " diff to norm: " + str(normal - angle) + " back curve: " + str(curve)

        #recalibrate command
        elif input == "calibrate":
            normal = calibrate(4)

        #quit command
        elif input == "quit":
            break

if __name__ == '__main__':
    cap = cv2.VideoCapture("/dev/video1")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    #multiprocessing management
    data = Process(target = dataloop)
    webcam = Process(target = record)
    data.start()
    webcam.start()
    data.join()
    webcam.terminate()


    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
