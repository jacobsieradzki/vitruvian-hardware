import smbus
import FaBo9Axis_MPU9250 as MPU
from Reading import Reading

bus = smbus.SMBus(1)
address = 0x70
mpu = MPU.MPU9250()


class MPUInputSource:
    def __init__(self, path, received_new_reading): #, recieved_new_norm_reading):
        self.path = path
        self.received_new_reading = received_new_reading
        bus.write_byte(address, self.path)

    def fetch_new_reading(self, timestamp, calibrate=False):
        bus.write_byte(address, self.path)
        acceleration = mpu.readAccel()
        x = acceleration['x'] + 0.00000001
        y = acceleration['y'] + 0.00000001
        z = acceleration['z'] + 0.00000001
        self.received_new_reading(Reading(timestamp, x, y, z), calibrate=calibrate)
