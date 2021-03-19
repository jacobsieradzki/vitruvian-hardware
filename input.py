
class Reading:
    def __init__(self, data):
        self.timestamp = data['timestamp']
        self.x = data['x'] + 0.00000001
        self.y = data['y'] + 0.00000001
        self.z = data['z'] + 0.00000001


class MpuReader:
    def __init__(self, bus, dev, addr, mpu):
        self.results = []
        for j in dev:
            bus.write_byte(addr, j)
            reading = Reading(mpu.readAccel())
            self.results.append(reading)
