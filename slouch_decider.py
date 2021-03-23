#Python class for setting up slouch deciders. Slouch deciders determine if a user is slouching
#   based on back measurements

import back_measurement

ANGLE_THRESHOLD = 0
CURVE_THRESHOLD = 0

class slouch_decider:
    def __init__(self, norm_angle, norm_curve):
        self.norm_angle = norm_angle
        self.norm_curve = norm_curve
        self.counter = 0

    #Given the absolute differences between observed and normal values, decides if slouching has occured
    def slouching(self, reading1, reading2):
        (angle, curve) = back_measurement.calculate_measurements(reading1, reading2)
        (angle_diff, curve_diff) = back_measurement.calculate_differences(self.norm_angle, self.norm_curve, angle, curve)
        if angle_diff > ANGLE_THRESHOLD and curve_diff > CURVE_THRESHOLD:
            print("slouching in decider")
            return True
        else:
            return False

    #Decides the users progress towards a slouch output, returning true if the user is slouching,
    #   returning false and updating the counter if not.
    def decide(self, reading1, reading2):
        print("counter = ", self.counter)
        if self.slouching(reading1, reading2):
            self.counter += 0.02
        else:
            self.counter -= 0.01
        if self.counter >= 4:
            self.counter = 0
            return True
        else:
            return False