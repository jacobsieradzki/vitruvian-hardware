import numpy as np
from ml_kit import *
import ml_kit as ml

#pre-processed data
#35 minutes of SITTING
#7 miutes of STANDING 
#23 miutes of ACTIVITIES
#labelled with SITTING, STANDING and ACTIVE: 3,4,0
with open('./sedentary_testsets/test.npy', 'rb') as f:
    X = np.load(f)
    y = np.load(f)

#load model
model = Model('./ml_models/cnn_model')

#predict
y_pred = model.predict(X)

print(f'test data shape {X.shape}')

#evaluate
ml.sedentary_accuracy(y, y_pred)