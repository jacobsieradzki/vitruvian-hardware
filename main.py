# main.py
import sys
import time
from input import get_input_sources
from ActivityType import ActivityType

# python3 main.py MOCK_MPU1 MOCK_MPU2 BLUETOOTH
# python3 main.py LIVE LIVE BLUETOOTH
# python3 main.py pi/accel-lower-jakevid1.csv pi/accel-upper-jakevid1.csv BLUETOOTH


INTERVAL_MS = 500


if len(sys.argv) != 4:
    sys.exit("Incorrect arguments. Use:\n" + sys.argv[0] + " [MPU1_SOURCE] [MPU2_SOURCE] [OUTPUT]")


output_location = sys.argv[3]
buffer_file = ""
rel_time = 0
mpu1_readings = []
mpu2_readings = []


def add_to_buffer(activity_type, value=None):
    global buffer_file
    item = "; " if len(buffer_file) > 0 else ""
    if value is None:
        item += str(activity_type) + " " + str(rel_time)
    else:
        item += str(activity_type) + " " + str(rel_time) + " " + str(value)
    buffer_file += item
    print("### file")
    print(buffer_file)


slouch_detection = ExampleDetectionAlgorithm(add_to_buffer)
sedentary_detection = ExampleDetectionAlgorithm(add_to_buffer)


def received_readings():
    if len(mpu1_readings) < 1 or len(mpu2_readings) < 1:
        return

    mpu1_reading, mpu2_reading = mpu1_readings.pop(0), mpu2_readings.pop(0)
    slouch_detection.add_new_reading(mpu1_reading, mpu2_reading)
    sedentary_detection.add_new_reading(mpu2_reading)


def received_new_mpu1_reading(reading):
    print("# received_new_mpu1_reading", reading.timestamp, reading.x, reading.y, reading.z)
    mpu1_readings.append(reading)
    received_readings()


def received_new_mpu2_reading(reading):
    print("# received_new_mpu2_reading", reading.timestamp, reading.x, reading.y, reading.z)
    mpu2_readings.append(reading)
    received_readings()


mpu1_source, mpu2_source = get_input_sources(sys.argv[1], sys.argv[2],
                                             received_new_mpu1_reading, received_new_mpu2_reading)

while True:
    mpu1_source.fetch_new_reading(rel_time, INTERVAL_MS)
    mpu2_source.fetch_new_reading(rel_time, INTERVAL_MS)

    rel_time += INTERVAL_MS
    time.sleep(INTERVAL_MS / 1000)
