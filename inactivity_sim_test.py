from ml_kit import *
import ml_kit as ml
import pandas as pd

SIM_GRAVITY = 9.81

#load data
sim_data = pd.read_csv('./sim_datasets/simulation.csv', names = ['x', 'y', 'z'])
sim_data = sim_data.div(SIM_GRAVITY, axis= 0) #ignore gravity
sim_data['label'] = 3 #SITTING

#normalise data
norm = Normaliser('ml_models/scaler.save')
data, labels = norm.normalise(sim_data)

#segment data into frames of 4 seconds
freq = 50 #Hertz
data, y_true = ml.get_frames(data, labels, freq*4, freq*2)

#load model
model = Model('./ml_models/cnn_model')

#predict
y_pred = model.predict(data)

#evaluate
ml.sedentary_accuracy(y_true, y_pred)