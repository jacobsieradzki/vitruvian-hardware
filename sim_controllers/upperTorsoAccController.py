"""upperTorsoAcc controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Emitter, Receiver, Accelerometer
import struct
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)
upperTorsoAcc = robot.getDevice("upperTorsoAcc")
upperTorsoAcc.enable(timestep)
upperTorsoRec = robot.getDevice("upper_receiver")
upperTorsoRec.enable(timestep)
upperTorsoEmit = robot.getDevice("upper_emitter")


sample = False

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    
    #wait for data request, when any signal received, move to read sensors
    if (upperTorsoRec.getQueueLength() > 0):
        sample = True
        #clear queue
        upperTorsoRec.nextPacket()

    # read the sensor data
    if (sample == True) :
        #get acc values
        acc_values = upperTorsoAcc.getValues()
        #package for sending
        accel_values = struct.pack("fff",acc_values[0],acc_values[1],acc_values[2])
        #send back to other accelerometer
        upperTorsoEmit.send(accel_values)
        sample = False
       
    pass

# Enter here exit cleanup code.