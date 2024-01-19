import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
model = tf.keras.models.load_model('DenseNetApproach.h5')

import numpy as np
img = image.load_img("iii.jpg",target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)
    
predictions = model.predict(img_array)
print(predictions)