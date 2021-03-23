# main.py
import sys
import time
from input import get_input_sources
from ActivityType import ActivityType
from back_measurement import calculate_norm
import slouch_buffer
import slouch_decider

INTERVAL_MS = 500
CAL_LENGTH_MS = 4000

# python3 main.py MOCK_MPU1 MOCK_MPU2 MOCK_GYRO BLUETOOTH

if len(sys.argv) != 5:
    sys.exit("Incorrect arguments. Use:\npython3 " + sys.argv[0] + " [MPU1_SOURCE] [MPU2_SOURCE] [GYRO_SOURCE] [OUTPUT]")

output_location = sys.argv[4]
buffer_file = ""
rel_time = 0
mpu1_readings = []
mpu2_readings = []
gyro_readings = []

mpu1_norm_readings = []
mpu2_norm_readings = []

decider = slouch_decider.slouch_decider(0, 0)

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

def received_readings():
    if len(mpu1_readings) < 1 or len(mpu2_readings) < 1:
        return

    print("here")
    mpu1_reading, mpu2_reading, gyro_reading = mpu1_readings.pop(0), mpu2_readings.pop(0), gyro_readings.pop(0)
    slouch_detection_reading(mpu1_reading, mpu2_reading)
    sedentary_detection_reading(mpu1_reading, mpu2_reading, gyro_reading)


def slouch_detection_reading(mpu1_reading, mpu2_reading):
    if slouch_decider.decide(mpu1_reading, mpu2_reading):
        print("### slouch_detection ...", mpu1_reading, mpu2_reading)
        add_to_buffer(ActivityType.SLOUCH_ALERT)
        score = slouch_buffer.update_buffer(True)
        if score == 0 or score:
            add_to_buffer(ActivityType.POSTURE, value=score)
    else:
        score = slouch_buffer.update_buffer(False)
        if score == 0 or score:
            add_to_buffer(ActivityType.POSTURE, value=score)
    # add_to_buffer(ActivityType.POSTURE, 55)


def sedentary_detection_reading(mpu1_reading, mpu2_reading, gyro_reading):
    print("### sedentary_detection_reading ...", mpu1_reading, mpu2_reading, gyro_reading)
    # add_to_buffer(ActivityType.WALKING)


def received_new_mpu1_reading(reading, calibrate=False):
    print(calibrate)
    print("# received_new_mpu1_reading", reading.timestamp, reading.x, reading.y, reading.z)
    if(calibrate):
        mpu1_norm_readings.append(reading)
    else:
        mpu1_readings.append(reading)
        received_readings()


def received_new_mpu2_reading(reading, caibrate=False):
    print("# received_new_mpu2_reading", reading.timestamp, reading.x, reading.y, reading.z)
    if(calibrate):
        mpu2_norm_readings.append(reading)
    else:
        mpu2_readings.append(reading)
        received_readings()


def received_new_gyro_reading(reading):
    print("# received_new_gyro_reading", reading.timestamp, reading.x, reading.y, reading.z)
    gyro_readings.append(reading)
    received_readings()


mpu1_source, mpu2_source, gyro_source = get_input_sources(
    sys.argv[1], sys.argv[2], sys.argv[3],
    received_new_mpu1_reading, received_new_mpu2_reading, received_new_gyro_reading
)

def calibrate():
    i = 0
    while i < CAL_LENGTH:
        mpu1_source.fetch_new_reading(rel_time, INTERVAL_MS, calibrate=True)
        mpu2_source.fetch_new_reading(rel_time, INTERVAL_MS, calibrate=True)

        time.sleep(INTERVAL_MS / 1000)
    readings = zip(mpu1_norm_readings, mpu2_norm_readings)
    norm = calculate_norm()
    slouch_decider.norm_angle = norm[0]
    slouch_decider.norm_curve = norm[1]
    mpu1_norm_readings.clear()
    mpu2_norm_readings.clear()

while True:
    mpu1_source.fetch_new_reading(rel_time, INTERVAL_MS)
    mpu2_source.fetch_new_reading(rel_time, INTERVAL_MS)
    gyro_source.fetch_new_reading(rel_time, INTERVAL_MS)

    rel_time += INTERVAL_MS
    time.sleep(INTERVAL_MS / 1000)
