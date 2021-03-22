#Python file containing methods for measuring angle and curve using accelerometer output
import math


#Given an accelerometer reading, calculates the accelerometers angle to the vertical on the plane
#   formed by the y and z axis'
def accel_to_angle(reading):
    angle = math.degrees(math.atan(reading.y/reading.z))
    if(angle > 0):
        return -90 + angle
    else:
        return 90 + angle

#Given two accelerometer inputs, calculates average back angle and curve
def calculate_measurements(reading1, reading2):
    angle1 = accel_to_angle(reading1)
    angle2 = accel_to_angle(reading2)
    angle = (angle1 + angle2) / float(2)
    curve = angle1 - angle2
    return (angle, curve)

#Given a list of reading pairs, returns calibrated normals for angle and curve
def calculate_norm(readings):
    angles = []
    curves = []
    i = 0
    while i < len(readings):
        reading1 = readings[i][0]
        reading2 = readings[i][1]
        (angle, curve) = calculate_measurements(reading1, reading2)
        angles.append(angle)
        curves.append(curve)
        i += 1
    norm_angle = sum(angles)/len(angles)
    norm_curve = sum(curves)/len(curves)
    print "Normal angle set to: " + str(norm_angle)
    print "Normal curve set to: " + str(norm_curve)
    print "\n"
    return (norm_angle, norm_curve)

#Given normal values for angle and curve, as well as measurements for angle and curve, return 
# absolute differneces between the measured and normal values
def calculate_differences(norm, measurements):
    (norm_angle, norm_curve) = norm
    (angle, curve) = measurements
    angle_diff = abs(angle - norm_angle)
    curve_diff = abs(curve - norm_curve)
    return (angle_diff, curve_diff)



