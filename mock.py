import requests
import re
from input import Reading
import json


INPUT_REGEX = "^([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+)$"
# BASE_URL = "https://vitruvian.jakeryan.co.uk/api/"
BASE_URL = "http://localhost:3000/api/"

# ----------------------------
# Fetch single reading
# ----------------------------


def fetchTestMpuReading(time, mpu_path):
    return fetchRemoteServerReading(mpu_path + "?time=" + str(time))


def fetchLiveMpuReading(mpu_path):
    return fetchRemoteServerReading(mpu_path)


def fetchRemoteServerReading(path):
    r = requests.get(BASE_URL + path)
    matches = re.findall(INPUT_REGEX, r.text)
    if r.status_code == 200 and matches is not None and len(matches) == 1 and len(matches[0]) == 4:
        [(timestamp, x, y, z)] = matches
        return Reading({'x': float(x), 'y': float(y), 'z': float(z)})
    else:
        return Reading({'x': 0, 'y': 0, 'z': 0})


# ----------------------------
# Fetch single reading
# ----------------------------


def fetchLiveMpuReadings(path):
    r = requests.get(BASE_URL + path)
    if r.status_code == 200 and len(r.text) > 0:
        data = json.loads(r.text)
        data = list(map(lambda o: Reading({'timestamp': float(o['timestamp']), 'x': o['x'], 'y': o['y'], 'z': o['z']}), data))
        data.sort(key=lambda x: x.timestamp, reverse=True)
        return data
    else:
        return []


# ----------------------------
# Post buffer file
# ----------------------------


def postToRemoteDatabase(key, buffer_file):
    data = buffer_file
    url = BASE_URL + "pi/" + key
    try:
        r = requests.post(url, data=data)
        print('Received ' + str(r.status_code) + ' status code from remote database for POST')
        print(r.text)
        return r.text == data

    except requests.exceptions.RequestException as e:
        print("Error posting to remote database: " + str(e))
        return False
