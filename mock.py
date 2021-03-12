import requests
import re
from input import Reading
import json


INPUT_REGEX = "^([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+),([-+]?[0-9]*\.[0-9]+|[0-9]+)$"
FIREBASE_BASE_URL = "https://vitruvian-38478-default-rtdb.europe-west1.firebasedatabase.app/"
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
    data = json.dumps(buffer_file)
    try:
        url = FIREBASE_BASE_URL + "tests/" + key + ".json"
        r = requests.put(url, data=data)
        return r.text == data

    except requests.exceptions.RequestException as e:
        print("Error posting to remote database: " + e)
        return False
