import numpy as np
from ml_kit import *
import ml_kit as ml
import sedentary_buffer



#load model
model = LiteModel('./ml_models/model.tflite')

X = sedentary_buffer.load_buffer()

FREQ = 4
DUR = 20 #duration in minutes
ACTIVE_DUR = 10
def classify():
    for x in X:
        #predict
        sedentary_buffer.get_next()
        y_pred = model.predict(x)
        print(f'classified as {sedentary_buffer.classes[y_pred]}')

sed_count = 0
sed_count_limit = DUR*60/FREQ
active_count = 0
active_count_limit = ACTIVE_DUR*60/FREQ

while True:
    classify()
    if (y_pred == 3 or y_pred == 4 or y_pred == 5):
        sed_count += 1
        if(sed_count >= sed_count_limit):
            #call send notification function here
            sed_count = 0

    else:
        active_count += 1
        if(active_count >= active_count_limit):
            sed_count = 0
            active_count = 0

    }