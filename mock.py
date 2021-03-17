import requests
import re
from input import Reading
import json


INPUT_REGEX = "^([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+)$"
# BASE_URL = "https://vitruvian.jakeryan.co.uk/api/"
BASE_URL = "http://localhost:3000/api/"


def fetchTestMpuReading(time, mpu_path):
    return fetchRemoteServerReading(mpu_path + "?time=" + str(time))


def fetchRemoteServerReading(path):
    r = requests.get(BASE_URL + path)
    matches = re.findall(INPUT_REGEX, r.text)
    if r.status_code == 200 and matches is not None and len(matches) == 1 and len(matches[0]) == 4:
        [(timestamp, x, y, z)] = matches
        return Reading({'x': float(x), 'y': float(y), 'z': float(z)})
    else:
        return Reading({'x': 0, 'y': 0, 'z': 0})


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
