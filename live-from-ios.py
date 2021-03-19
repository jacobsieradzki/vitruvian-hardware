import time
from mock import fetchLiveMpuReadings, BASE_URL

FREQ = 100
CURRENT_TEST_KEY = "demo-3-test"
MPU1_RESOURCE_PATH = "ios/accel-jake?format=ALL"
MPU2_RESOURCE_PATH = "ios/gyro-jake?format=ALL"


def receivedSensorReading(o, t):
    print("")
    print("###")
    print("Time = " + str(t) + " (" + str(t/1000) + "s)")
    print("MPU1 = x={x:.5f}, y={y:.5f}, z={z:.5f}".format(x=o[0].x, y=o[0].y, z=o[0].z))
    print("MPU2 = x={x:.5f}, y={y:.5f}, z={z:.5f}".format(x=o[1].x, y=o[1].y, z=o[1].z))


print('Reading mock MPU1 and MPU2 ...\n')
print('... from ' + BASE_URL + MPU1_RESOURCE_PATH)
print('... from ' + BASE_URL + MPU2_RESOURCE_PATH)
print('')

app_readings = []
timestamp = 0 # ms

while True:
    mpu1_readings = fetchLiveMpuReadings(MPU1_RESOURCE_PATH)
    mpu2_readings = fetchLiveMpuReadings(MPU2_RESOURCE_PATH)
    results = list(zip(mpu1_readings, mpu2_readings))

    for mpu1, mpu2 in results:
        diff = abs(float(mpu1.timestamp) - float(mpu2.timestamp))
        if diff > 50:
            continue

        receivedSensorReading([mpu1, mpu2], timestamp)

        timestamp += FREQ
        time.sleep(FREQ / 1000)

    if len(results) == 0:
        print("")
        print("###")
        print("No updates...")
        timestamp += 1000
        time.sleep(1)
