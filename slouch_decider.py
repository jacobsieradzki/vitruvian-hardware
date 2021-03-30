#Python class for setting up slouch deciders. Slouch deciders determine if a user is slouching
#   based on back measurements

import back_measurement

class slouch_decider:
    def __init__(self, norm_angle, norm_curve, interval_ms, angle_threshold=0, curve_threshold=0):
        if interval_ms >= 4000:
            raise ValueError("interval cannot be more than 4000 milliseconds")
        self.norm_angle = norm_angle
        self.norm_curve = norm_curve
        self.angle_threshold = angle_threshold
        self.angle_threshold = angle_threshold
        self.counter = 0
        self.interval_ms = interval_ms

    #Given the absolute differences between observed and normal values, decides if slouching has occured
    def slouching(self, reading1, reading2):
        (angle, curve) = back_measurement.calculate_measurements(reading1, reading2)
        (angle_diff, curve_diff) = back_measurement.calculate_differences(self.norm_angle, self.norm_curve, angle, curve)
        if angle_diff > self.angle_threshold and curve_diff > self.angle_threshold:
            print("slouching in decider")
            return True
        else:
            return False

    #Decides the users progress towards a slouch output, returning true if the user is slouching,
    #   returning false and updating the counter if not.
    def decide(self, reading1, reading2):
        print("counter = ", self.counter)
        if self.slouching(reading1, reading2):
            self.counter += self.interval_ms
        else:
            self.counter -= self.interval_ms / float(2)
        if self.counter >= 4000:
            self.counter = 0
            return True
        else:
            return False