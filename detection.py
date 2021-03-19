from picamera import PiCamera
import time
import sys
import FaBo9Axis_MPU9250 as MPU
from datetime import datetime
import math
import smbus
import os
import slouch_buffer

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
#idnetifier for device currently selected
device_select = 0

#initialise camera and mpu at first mux position
camera = PiCamera()

def accel_to_angle(y, z):
    angle = math.degrees(math.atan(y/z))
    if(angle > 0):
        return -90 + angle
    else:
        return 90 + angle
    
#Returns calibrated normals for angle and curve
def calibrate(cal_length) :
    norm = 0
    i = 0
    cal_angles = []
    cal_curves = []
    while i < cal_length:
        theta = []
        print i
        #loop for both devices, add the appropriate values to the recorded values
        for j in dev:
            bus.write_byte(addr,j)
            accel = mpu.readAccel()
            y = accel['y'] + 0.00000001
            z = accel['z'] + 0.00000001
            theta.append(accel_to_angle(y, z))
        angle = sum(theta)/len(theta)
	print str(angle)
	curve = theta[0] - theta[1]
	print str(curve)
        #get the average angle of the sensors
        cal_angles.append(angle)
        cal_curves.append(curve)
        time.sleep(0.25)
        i+=0.25
    #get the average over all readings
    norm_angle = sum(cal_angles)/len(cal_angles)
    norm_curve = sum(cal_curves)/len(cal_curves)
    print "Normal angle set to: " + str(norm_angle)
    print "Normal curve set to: " + str(norm_curve)
    print "\n"
    return (norm_angle, norm_curve)

#Returns (angle, curve) as a tuple
def read(norm):
    norm_angle = norm[0]
    norm_curve = norm[1]
    angle = 0
    curve = 0
    theta = []
    #loop through IMUs and calculate angle of each
    for j in dev:
        bus.write_byte(addr, j)
        accel = mpu.readAccel()
        y = accel['y'] + 0.00000001
        z = accel['z'] + 0.00000001
        theta.append(accel_to_angle(y, z))
    #calculate average back angle and curve
    angle = sum(theta)/len(theta)
    ang_to_norm = angle - norm_angle
    curve_to_norm = theta[0] - theta[1] - norm_curve
    return (ang_to_norm, curve_to_norm)

def over_threshold(reading):
    if(abs(reading[0]) > 10 and abs(reading[1]) > -15):
        return True
    else:
        return False

#Deprecated method
#def or_over_threshold(reading):
#    if(abs(reading[0]) > 10 or abs(reading[1]) > 10):
#        return True
#    else:
#        return False

def main():
    norm = (0, 0)
    #Wait for user to start calibration
    print "Type 'cal' to begin calibration"
    while(True):
        if(raw_input() == 'cal'):
        print "calibrating"
            norm = calibrate(4)
            print "calibration finished"
            #Bluetooth connection goes here
            break

    cam = False
    #Wait for user to specify if camera is desired (for testing purposes)
    print "Type 'cam' for streaming and recording, and 'nocam' otherwise"
    while(True):
        input  = raw_input()
        if(input == 'cam'):
            #Turn the thing on
        cam = True
        break
        elif(input == 'nocam'):
            print "nocam"
            #Nocam
        break

    #Enter slouch detection loop
    counter = 0
    print_counter = 0
    while(True):
        print_counter += 0.25
        if(counter >= 4):
            and_counter = 0
            print("----------------------------------")
            print "slouching detected
            print("----------------------------------")
            slouch_buffer.update_buffer()
        os.system("python3 anglebuzz.py")
        if(input == "quit"):
            break
        reading = read(norm)
        if(print_counter >= 2):
        print reading 
        print_counter = 0
        if(over_threshold(reading)):
            counter += 0.25
        elif(counter > 0):
            counter -= 0.125
        time.sleep(0.25)

    if(cam):
        #Turn off the camera
        1

if __name__ == "__main__":
    #Execute only if run as a script
    main()