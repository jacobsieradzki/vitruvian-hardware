import time
import numpy as np

classes = {
    0 : "WALKING",
    1 : "WALKING_UPSTAIRS",
    2 : "WALKING_DOWNSTAIRS",
    3 : "SITTING",
    4 : "STANDING",
    5 : "LAYING",
    6 : "STAND_TO_SIT",
    7 : "SIT_TO_STAND",
    8 : "SIT_TO_LIE",
    9 : "LIE_TO_SIT",
    10 : "STAND_TO_SIT",
    11 : "LIE_TO_STAND"
}

def load_buffer():
    with open('./sedentary_testsets/liteSamples.npy', 'rb') as f:
        return np.load(f)

def get_next():
    time.sleep(2)
