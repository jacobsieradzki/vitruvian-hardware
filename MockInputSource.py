import requests
import re
from Reading import Reading
from mock import BASE_URL

INPUT_REGEX = "^([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+)$"


class MockInputSource:
    def __init__(self, path, received_new_reading):
        self.path = path
        self.received_new_reading = received_new_reading

    def fetch_new_reading(self, timestamp, interval):
        url = BASE_URL + self.path + "?timestamp=" + str(timestamp) + "&interval=" + str(interval)
        r = requests.get(url)
        matches = re.findall(INPUT_REGEX, r.text)

        if r.status_code == 200 and matches is not None and len(matches) == 1 and len(matches[0]) == 4:
            [(timestamp, x, y, z)] = matches
            reading = Reading(timestamp, float(x), float(y), float(z))
            self.received_new_reading(reading)

        else:
            print("Error: ", url, r.status_code)
            reading = Reading(timestamp, 0, 0, 0)
            self.received_new_reading(reading)

