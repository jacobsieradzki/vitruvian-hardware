from ActivityType import ActivityType


class ExampleDetectionAlgorithm:
    def __init__(self, add_to_buffer_file):
        self.mpu1_readings = []
        self.mpu2_readings = []
        self.add_to_buffer_file = add_to_buffer_file

    def add_new_reading(self, mpu1_reading, mpu2_reading):
        self.mpu1_readings.append(mpu1_reading)
        self.mpu2_readings.append(mpu2_reading)

        # process values ...

        self.add_to_buffer_file(ActivityType.POSTURE, 55)
        self.add_to_buffer_file(ActivityType.WALKING_DOWNSTAIRS)

