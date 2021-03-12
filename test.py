from mock import fetchTestMpuReading, postToRemoteDatabase, BASE_URL

CURRENT_TEST_KEY = "jake-test"
MPU1_RESOURCE_PATH = "pi/test1_mpu1"
MPU2_RESOURCE_PATH = "pi/test1_mpu2"


def printReadings(o):
    print("MPU1 = x={x:.5f}, y={y:.5f}, z={z:.5f}".format(x=o[0].x, y=o[0].y, z=o[0].z))
    print("MPU2 = x={x:.5f}, y={y:.5f}, z={z:.5f}".format(x=o[1].x, y=o[1].y, z=o[1].z))


def fetchReadings():
    mpu1_readings = fetchTestMpuReading(timestamp, MPU1_RESOURCE_PATH)
    mpu2_readings = fetchTestMpuReading(timestamp, MPU2_RESOURCE_PATH)
    return [mpu1_readings, mpu2_readings]


def performSlouchDetection(result, t, r, n):
    result.append([0, t, 50])
    print("!!! Adding fake POSTURE event value=50")
    print("!!! 0 " + str(t) + " " + str(50) + ";")
    print("")


print('Reading mock MPU1 and MPU2 ...\n')

app_readings = []
timestamp = 0 # ms

while timestamp < 10000:
    readings = fetchReadings()

    print("Time = " + str(timestamp) + " (" + str(timestamp/1000) + "s)")
    printReadings(readings)

    output = []

    normal = 0
    performSlouchDetection(app_readings, timestamp, readings, normal)

    timestamp += 500 # ms


# Upload to Firebase
output = ';'.join(list(map(lambda x: ' '.join(list(map(lambda y: str(y), x))), app_readings)))
print("Uploading to remote server id=" + CURRENT_TEST_KEY + "...")
postToRemoteDatabase(CURRENT_TEST_KEY, output)
print("Uploaded to remote server, available at " + BASE_URL + "app/" + CURRENT_TEST_KEY)
