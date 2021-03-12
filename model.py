import tesnorflow as tf

class Model:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path="model.tflite")
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = interpreter.get_input_details()
        self.output_details = interpreter.get_output_details()
        self.input_shape = input_details[0]['shape']

    def predict(self, input_data):
        input_data = np.array(input_data.reshape(1, 200, 3, 1),dtype=np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        results = np.squeeze(output_data)
        top_k = results.argsort()[-5:][::-1]
        return top_k[0]
