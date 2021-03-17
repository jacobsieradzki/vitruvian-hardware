import tensorflow as tf
import joblib
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import accuracy_score, recall_score, f1_score

def sedentary_accuracy(y_true, y_pred):
    
    sedentary = [3, 4, 5] # Sitting, STANDING and LAYING
    y_true = np.array([0 if x in sedentary else 1 for x in y_true])
    y_pred = np.array([0 if x in sedentary else 1 for x in y_pred])
    
    acc = accuracy_score(y_true, y_pred)

    print(f'The model achieved a sedentary accuracy score of {acc*100}%')
    if acc < 1.0:
        print(f'A recall score of {recall_score(y_true, y_pred)*100}%')
        print(f'And an F1 score of {f1_score(y_true, y_pred)*100}%')

def get_frames(data, labels, frame_size, hop_size):
    data['label'] = labels
    
    N_FEATURES = 3

    frames = []
    labels = []
    for i in range(0, len(data) - frame_size, hop_size):    
        x = data['x'].values[int(i): int(i + frame_size)]
        y = data['y'].values[i: i + frame_size]
        z = data['z'].values[i: i + frame_size]
        
        # Retrieve the most often used label in this segment
        label = stats.mode(data['label'][i: i + frame_size])[0][0]
        frames.append([x, y, z])
        labels.append(label)

    frames = np.asarray(frames).reshape(-1, frame_size, N_FEATURES)
    labels = np.asarray(labels)

    return frames, labels

class Normaliser:
    def __init__(self, normaliser_path):
        self.scaler = joblib.load(normaliser_path)

    def normalise(self, data):
        labels = data['label']
        data = data[['x', 'y', 'z']]
        data = self.scaler.transform(data)
        return pd.DataFrame(data=data, columns = ['x', 'y', 'z']), labels

class Model:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, data): # imput data must be in the shape (n, 200, 3)
        data = data.reshape(data.shape[0], 200, 3, 1)
        return self.model.predict_classes(data)
        
class LiteModel:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = interpreter.get_input_details()
        self.output_details = interpreter.get_output_details()
        self.input_shape = input_details[0]['shape']

    def predict(self, input_data): #input data must be a np array in the shape (200, 3)
        input_data = np.array(input_data.reshape(1, 200, 3, 1),dtype=np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        results = np.squeeze(output_data)
        top_k = results.argsort()[-5:][::-1]
        return top_k[0]
