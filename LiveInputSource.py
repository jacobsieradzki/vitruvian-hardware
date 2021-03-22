from mock import fetchLiveMpuReadings, BASE_URL


class LiveInputSource:
    def __init__(self, path, received_new_reading):
        self.path = path
        self.received_new_reading = received_new_reading
        self.readings = []
        self.last_fetched_count = 0

    def fetch_new_reading(self, timestamp, interval):
        if self.last_fetched_count == 0:
            new_readings = fetchLiveMpuReadings(self.path)
            self.last_fetched_count = len(new_readings)
            print("Received " + str(self.last_fetched_count) + " live readings, " + str(len(self.readings)) + " pending...")

            for reading in new_readings:
                self.readings.append(reading)

        if len(self.readings) > 0:
            r = self.readings.pop(0)
            self.received_new_reading(r)
        else:
            self.last_fetched_count = 0
