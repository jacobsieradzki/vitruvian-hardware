from Reading import Reading


class MPUInputSource:
    def __init__(self, path, received_new_reading):
        import smbus
        import FaBo9Axis_MPU9250 as MPU

        self.bus = smbus.SMBus(1)
        self.address = 0x70
        self.mpu = MPU.MPU9250()
        self.path = path
        self.received_new_reading = received_new_reading
        self.bus.write_byte(self.address, self.path)

    def fetch_new_reading(self, timestamp, calibrate=False):
        self.bus.write_byte(self.address, self.path)
        acceleration = self.mpu.readAccel()
        x = acceleration['y'] + 0.00000001
        y = acceleration['y'] + 0.00000001
        z = acceleration['z'] + 0.00000001
        self.received_new_reading(Reading(timestamp, x, y, z), calibrate=calibrate)
