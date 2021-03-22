#Python class for setting up slouch deciders. Slouch deciders determine if a user is slouching
#   based on back measurements

import back_measurement

ANGLE_THRESHOLD = 10
CURVE_THRESHOLD = 15

class slouch_decider:
    def __init__(norm):
        self.norm = norm
        self.counter = 0

    #Given the absolute differences between observed and normal values, decides if slouching has occured
    def slouching(readings) 
        (angle_diff, curve_diff) = back_measurement.calculate_differences(self.norm, readings)
        if angle_diff > ANGLE_THRESHOLD and curve_diff > 15:
            return True
        else:
            return False

    #Decides the users progress towards a slouch output, returning true if the user is slouching,
    #   returning false and updating the counter if not.
    def decide(readings):
        if slouching(reading):
            self.counter += 0.25
        else:
            self.counter -= 1.25
        if self.counter >= 4:
            self.counter = 0
            return True
        else:
            return False