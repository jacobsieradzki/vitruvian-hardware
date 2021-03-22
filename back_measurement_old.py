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

#initialise camera and mpu at first mux position
camera = PiCamera()

def accel_to_angle(y, z):
    angle = math.degrees(math.atan(y/z))
    if(angle > 0):
        return -90 + angle
    else:
        return 90 + angle
    
#Returns calibrated normals for angle and curve
def calibrate(cal_length, reader) :
    norm = 0
    i = 0
    cal_angles = []
    cal_curves = []
    while i < cal_length:
        print i
        (angle, curve) = reader()
	    print str(angle)
	    print str(curve)
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

#Returns (angle, curve) as a tuple, adjusted based on difference from norm
def read(norm, reader):
    norm_angle = norm[0]
    norm_curve = norm[1]
    (angle, curve) = reader()
	print str(angle)
	print str(curve)
    ang_to_norm = angle - norm_angle
    curve_to_norm = curve - norm_curve
    return (ang_to_norm, curve_to_norm)

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