"""middleTorsoAcc controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Emitter, Receiver, Accelerometer
import struct
import math

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

#initialise the devices appropriately
middleTorsoAcc = robot.getDevice("middleTorsoAcc")
middleTorsoAcc.enable(timestep)
middleTorsoEmit = robot.getDevice("middle_emitter")
middleTorsoRec = robot.getDevice("middle_receiver")
middleTorsoRec.enable(timestep)


def accel_to_angle(y, z):
    angle = math.degrees(math.atan(y/z))
    if(angle > 0):
        return -90 + angle
    else:
        return 90 + angle
           
###I removed the whole calibration step, difficult to calibrate when system
###constantly moving. So I simply held it still and manually calculated normals
###and hardcoded them
norm = (-1.445, 14.35)
    
#Returns (angle, curve) as a tuple
def read(norm):
    norm_angle = norm[0]
    norm_curve = norm[1]
    angle = 0
    curve = 0
    theta = []
    #read local data
    accel = middleTorsoAcc.getValues()
    y = accel[1] + 0.00000001
    z = accel[2] + 0.00000001
    theta.append(accel_to_angle(y, z))
    #fetch data from other accelerometer (reformat to be readable)
    accel = struct.unpack("fff",middleTorsoRec.getData()) 
    #remove data from queue (necessary to keep if statements in detection
    #code happy)
    middleTorsoRec.nextPacket()
    #read other acc data
    y = accel[1] + 0.00000001
    z = accel[2] + 0.00000001
    theta.append(accel_to_angle(y, z))
    #calculate average back angle and curve as usual 
    angle = sum(theta)/len(theta)
    ang_to_norm = angle - norm_angle
    curve_to_norm = theta[0] - theta[1] - norm_curve
    #print("curve to norm is: " + str(curve_to_norm))
    #print("angle to norm is: " + str(ang_to_norm))
    return (ang_to_norm, curve_to_norm)

#same algorithm as pi
def and_detect(reading):
    if(abs(reading[0]) > 10 and abs(reading[1]) > -15):
        return True
    else:
        return False

#same algorithm as pi
def or_detect(reading):
    if(abs(reading[0]) > 10 or abs(reading[1]) > 10):
        return True
    else:
        return False
        
    
#initialise pre-while loop variables
print("past loop")
#Enter slouch detection loop
and_counter = 0
or_counter = 0
print_counter = 0

#extra variable to simulate our system, keeps track of time and thus
#when readings should be taken
timer = 0;

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    #increment timer
    timer += timestep
    
    #4 times a second (every 250ms) run our detection code
    if(timer%250 ==  0):
        print_counter += 0.25
        if(and_counter >= 4):
            and_counter = 0
            print("----------------------------------")
            print("slouching detected based on and metric")
            print("----------------------------------")
            #Bluetooth activty here
            #buzzbuzz
        if(or_counter >= 4):
            or_counter = 0
            print("----------------------------------")
            print("slouching detected based on or metric")
            print("----------------------------------")
            #Bluetooth activity here
            #buzzbuzz
        #other accelerometer will take a moment to prep data, so make the
        #request, then wait until it's ready to finish executing (see other if)
        message = "message".encode("utf-8")
        middleTorsoEmit.send(message)
           
    #wait for other accelerometer to be ready, then finish detection loop
    if(middleTorsoRec.getQueueLength() > 0):
        reading = read(norm)
        if(print_counter >= 2):
            print(reading) 
            print_counter = 0
        if(and_detect(reading)):
            and_counter += 0.25
        elif(and_counter > 0):
            and_counter -= 0.125
        if(or_detect(reading)):
            or_counter += 0.25
        elif(or_counter > 0):
            or_counter -= 0.125

        
    #acc_values = middleTorsoAcc.getValues()
    #print("----------------------------------")
    #print("Middle accelerometer values: {}".format(acc_values))
    
    pass

# Enter here exit cleanup code.
