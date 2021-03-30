# main.py
import sys
import time
from input import get_input_sources
from ActivityType import ActivityType
from back_measurement import calculate_norm
import slouch_buffer
import slouch_decider
from grove.button import Button
import grove.grove_ryb_led_button.GroveLedButton
import os
from mraa import getGpioLookup
from upm import pyupm_buzzer as upmBuzzer

INTERVAL_MS = 20
SLICE_LENGTH_MS = 20000
CAL_LENGTH_MS = 4000

# python3 main.py MOCK_MPU1 MOCK_MPU2 BLUETOOTH
# python3 main.py pi/accel-lower-jakevid1.csv pi/accel-upper-jakevid1.csv BLUETOOTH

if len(sys.argv) != 4:
    sys.exit("Incorrect arguments. Use:\npython3 " + sys.argv[0] + " [MPU1_SOURCE] [MPU2_SOURCE] [OUTPUT]")

output_location = sys.argv[3]
buffer_file = ""
rel_time = 0
mpu1_readings = []
mpu2_readings = []

mpu1_norm_readings = []
mpu2_norm_readings = []

decider = slouch_decider.slouch_decider(0, 0, INTERVAL_MS)
sbuffer = slouch_buffer.slouch_buffer(SLICE_LENGTH_MS)

led_button = GroveLedButton(5)
led_button.led.light(False)
normed = False
enabled = False
buzzer = upmBuzzer.Buzzer(getGpioLookup("GPIO%02d" % 12))

#handler for different button press events
def cust_on_event(index, event, tm):
    #print "event with code {}, time {}".format(event, tm)
    led_button.led.brightness = press.led.MAX_BRIGHT
    if (event & Button.EV_SINGLE_CLICK):
        #when single click and already calibrated normals, calibrate over_threshold
        if (normed):
            feedback(5)
            calibrate_threshold()
            normed = False
            feedback(3)
            led_button.led.light(True)
            enabled = True
    elif (event & Button.EV_LONG_PRESS):
        #when long press - calibrate the norms
        enabled = False
        feedback(5)
        calibrate()
        normed = True
        feedback(3)
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
    if len(mpu1_readings) < 1 or len(mpu2_readings) < 1:
        return

    mpu1_reading, mpu2_reading = mpu1_readings.pop(0), mpu2_readings.pop(0)
    slouch_detection_reading(mpu1_reading, mpu2_reading)
    #sedentary_detection_reading(mpu2_reading)


def slouch_detection_reading(mpu1_reading, mpu2_reading):
    print("### slouch_detection ...", mpu1_reading, mpu2_reading)
    if decider.decide(mpu1_reading, mpu2_reading):
        feedback(4)
        add_to_buffer(ActivityType.SLOUCH_ALERT)
        score = sbuffer.update_buffer(True)
        if score:
            add_to_buffer(ActivityType.POSTURE, value=score)
    else:
        score = sbuffer.update_buffer(False)
        if score:
            add_to_buffer(ActivityType.POSTURE, value=score)
    # add_to_buffer(ActivityType.POSTURE, 55)


#def sedentary_detection_reading(lower_mpu_reading):
    #print("### sedentary_detection_reading ...", lower_mpu_reading)
    # add_to_buffer(ActivityType.WALKING)


def received_new_mpu1_reading(reading, calibrate=False):
    print("# received_new_mpu1_reading", reading.timestamp, reading.x, reading.y, reading.z)
    if calibrate:
        mpu1_norm_readings.append(reading)
    else:
        mpu1_readings.append(reading)
        received_readings()


def received_new_mpu2_reading(reading, calibrate=False):
    print("# received_new_mpu2_reading", reading.timestamp, reading.x, reading.y, reading.z)
    if calibrate:
        mpu2_norm_readings.append(reading)
    else:
        mpu2_readings.append(reading)
        received_readings()


mpu1_source, mpu2_source = get_input_sources(sys.argv[1], sys.argv[2],
                                             received_new_mpu1_reading, received_new_mpu2_reading)

def calibrate():
    i = 0
    while i < CAL_LENGTH_MS:
        mpu1_source.fetch_new_reading(rel_time, INTERVAL_MS, calibrate=True)
        mpu2_source.fetch_new_reading(rel_time, INTERVAL_MS, calibrate=True)

        time.sleep(INTERVAL_MS / 1000)
    readings = zip(mpu1_norm_readings, mpu2_norm_readings)
    norm = calculate_norm()
    decider.norm_angle = norm[0]
    decider.norm_curve = norm[1]
    mpu1_norm_readings.clear()
    mpu2_norm_readings.clear()

def calibrate_threshold():
    i = 0
    while i < CAL_LENGTH_MS:
        mpu1_source.fetch_new_reading(rel_time, INTERVAL_MS, calibrate=True)
        mpu2_source.fetch_new_reading(rel_time, INTERVAL_MS, calibrate=True)

        time.sleep(INTERVAL_MS / 1000)
    readings = zip(mpu1_norm_readings, mpu2_norm_readings)
    norm = calculate_norm()
    decider.angle_threshold = norm[0] - decider.norm_angle
    decider.curve_threshold = norm[1] - decider.norm_curve
    mpu1_norm_readings.clear()
    mpu2_norm_readings.clear()


while True:
    if (enabled) :
        mpu1_source.fetch_new_reading(rel_time, INTERVAL_MS)
        mpu2_source.fetch_new_reading(rel_time, INTERVAL_MS)

    rel_time += INTERVAL_MS
    time.sleep(INTERVAL_MS / 1000)
