import back_measurement
import accel_read

def over_threshold(reading):
    if(abs(reading[0]) > 10 and abs(reading[1]) > -15):
        return True
    else:
        return False

norm
def calibrate(reader):
    global norm
    norm = back_measurement.calibrate(4, reader)

counter = 0
def decide(reader):
    global counter
    reading = back_measurement.read(norm, reader)
    if over_threshold(reading):
        counter += 0.25
    else:
        counter -= 1.25
    if counter >= 4:
        counter = 0
        return True