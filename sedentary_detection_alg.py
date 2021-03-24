import pandas as pd
from ml_kit import *
from ActivityType import ActivityType

class Algorithm:
    def __init__(self, duration, active_duration, add_to_buffer):
        self.readings = []
        self.segmet_size = 4 #seconds default
        self.dur = duration #duration in minutes
        self.active_dur = active_duration
        self.sed_count = 0
        self.sed_count_limit = self.dur*60/self.segmet_size
        self.active_count = 0
        self.active_count_limit = self.active_dur*60/self.segmet_size
        self.add_to_buffer = add_to_buffer
        self.last_pred = -1

        #load model
        self.model = LiteModel('./ml_models/model.tflite')

        #load normaliser
        self.norm = Normaliser('ml_models/scaler.save')

    def collect_readings(self, reading):
        if(len(self.readings) < 200):
            self.readings.append(reading)
        elif(len(self.readings) == 200):
            process()
            self.readings = []
        else:
            raise ValueError("Invalid Data Shape")

    def process(self):
        df = pd.Dataframe(columns = ['x', 'y', 'z'])
        for r in self.readings:
            df.append({'x': r.x, 'y': r.y, 'z': r.z}, ignore_index=True)
        
        data = self.norm.norm_x(df)

        y_pred = self.model.predict(x)
        
        if y_pred != self.last_pred:
            self.add_to_buffer(y_pred + 3)
            self.last_pred = y_pred
            
        if (y_pred == 3 or y_pred == 4 or y_pred == 5):
            self.sed_count += 1
            if(self.sed_count >= self.sed_count_limit):
                self.add_to_buffer(ActivityType.SIT_ALERT)
                self.sed_count = 0

        else:
            self.active_count += 1
            if(self.active_count >= self.active_count_limit):
                self.sed_count = 0
                self.active_count = 0
    
        


