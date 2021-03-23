# main.py
import sys
import time
from input import get_input_sources
from ActivityType import ActivityType
from grove.button import Button
import grove.grove_ryb_led_button.GroveLedButton
import os
from mraa import getGpioLookup
from upm import pyupm_buzzer as upmBuzzer

# python3 main.py MOCK_MPU1 MOCK_MPU2 MOCK_GYRO BLUETOOTH
# python3 main.py LIVE LIVE LIVE BLUETOOTH
# python3 main.py pi/accel-lower-jakevid1.csv pi/accel-upper-jakevid1.csv pi/gyro-lower-jakevid1.csv BLUETOOTH


INTERVAL_MS = 500


if len(sys.argv) != 5:
    sys.exit("Incorrect arguments. Use:\n" + sys.argv[0] + " [MPU1_SOURCE] [MPU2_SOURCE] [GYRO_SOURCE] [OUTPUT]")

output_location = sys.argv[4]
buffer_file = ""
rel_time = 0
mpu1_readings = []
mpu2_readings = []
gyro_readings = []
led_button = GroveLedButton(5)
led_button.led.light(False)
normed = False
buzzer = upmBuzzer.Buzzer(getGpioLookup("GPIO%02d" % 12))

#handler for different button press events
def cust_on_event(index, event, tm):
    #print "event with code {}, time {}".format(event, tm)
    led_button.led.brightness = press.led.MAX_BRIGHT
    if (event & Button.EV_SINGLE_CLICK):
        #when single click and already calibrated normals, calibrate over_threshold
        if (normed):
            ###call calibrate function here
            normed = False
            feedback(3)
            feedback(4)
            led_button.led.light(True)
    elif (event & Button.EV_LONG_PRESS):
        #when long press - calibrate the norms
        ###call calibrate function here
        normed = True
        feedback(3)
        feedback(4)
        led_button.led.blink()


#assign event handler to button object
led_button.on_event = cust_on_event

#function to play a corresponding note (and hopefully at a corresponding volume)
#numbers 0-7 correspond to notes do-si. all currently also use anglebuzz, but can be changed
def feedback(note_number, volume=500000):
    if (note_number == 0):
        buzzer.playSound(upmBuzzer.BUZZER_DO, volume)
        os.system("python3 anglebuzz.py") #could add new buzz files? or do we still need this if main.py is in python 3?
    elif (note_number == 1):
        buzzer.playSound(upmBuzzer.BUZZER_RE, volume
        os.system("python3 anglebuzz.py")
    elif (note_number == 2):
        buzzer.playSound(upmBuzzer.BUZZER_MI, volume)
        os.system("python3 anglebuzz.py")
    elif (note_number == 3):
        buzzer.playSound(upmBuzzer.BUZZER_FA, volume)
        os.system("python3 anglebuzz.py")
    elif (note_number == 4):
        buzzer.playSound(upmBuzzer.BUZZER_SOL, volume)
        os.system("python3 anglebuzz.py")
    elif (note_number == 5):
        buzzer.playSound(upmBuzzer.BUZZER_LA, volume)
        os.system("python3 anglebuzz.py")
    elif (note_number == 6):
        buzzer.playSound(upmBuzzer.BUZZER_SI, volume)
        os.system("python3 anglebuzz.py")

def add_to_buffer(activity_type, value=None):
    global buffer_file
    item = "; " if len(buffer_file) > 0 else ""
    if value is None:
        item += str(activity_type) + " " + str(rel_time)
    else:
        item += str(activity_type) + " " + str(rel_time) + " " + str(value)
    buffer_file += item
    print("### file", buffer_file)


def received_readings():
    if len(mpu1_readings) < 1 or len(mpu2_readings) < 1 or len(gyro_readings) < 1:
        return

    mpu1_reading, mpu2_reading, gyro_reading = mpu1_readings.pop(0), mpu2_readings.pop(0), gyro_readings.pop(0)
    slouch_detection_reading(mpu1_reading, mpu2_reading)
    sedentary_detection_reading(mpu2_reading, gyro_reading)


def slouch_detection_reading(mpu1_reading, mpu2_reading):
    print("### slouch_detection ...", mpu1_reading, mpu2_reading)
    # add_to_buffer(ActivityType.POSTURE, 55)


def sedentary_detection_reading(lower_mpu_reading, gyro_reading):
    print("### sedentary_detection_reading ...", lower_mpu_reading, gyro_reading)
    # add_to_buffer(ActivityType.WALKING)


def received_new_mpu1_reading(reading):
    # print("# received_new_mpu1_reading", reading.timestamp, reading.x, reading.y, reading.z)
    mpu1_readings.append(reading)
    received_readings()


def received_new_mpu2_reading(reading):
    # print("# received_new_mpu2_reading", reading.timestamp, reading.x, reading.y, reading.z)
    mpu2_readings.append(reading)
    received_readings()


def received_new_gyro_reading(reading):
    # print("# received_new_gyro_reading", reading.timestamp, reading.x, reading.y, reading.z)
    gyro_readings.append(reading)
    received_readings()


mpu1_source, mpu2_source, gyro_source = get_input_sources(
    sys.argv[1], sys.argv[2], sys.argv[3],
    received_new_mpu1_reading, received_new_mpu2_reading, received_new_gyro_reading
)


while True:
    mpu1_source.fetch_new_reading(rel_time, INTERVAL_MS)
    mpu2_source.fetch_new_reading(rel_time, INTERVAL_MS)
    gyro_source.fetch_new_reading(rel_time, INTERVAL_MS)

    rel_time += INTERVAL_MS
    time.sleep(INTERVAL_MS / 1000)
