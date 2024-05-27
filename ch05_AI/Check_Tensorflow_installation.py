import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

# Load your pre-trained model
model_path = r"./converted_keras/keras_model.h5"
model = load_model(model_path, compile=False)

# Load class names from labels file
labels_path = r"./converted_keras/labels.txt"
class_names = open(labels_path, "r").readlines()

# Confirm that TensorFlow and the model have loaded correctly
print('TensorFlow is installed correctly.')
print('Model loaded from:', model_path)
print('Class names:', class_names)
