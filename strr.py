import streamlit as st
from PIL import Image
import numpy as np
import your_skin_disease_model
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
model = tf.keras.models.load_model('DenseNetApproach.h5')
# Streamlit app header
st.title("Skin Disease Prediction")

# File upload widget
uploaded_file = st.file_uploader("Upload a skin condition image...", type=["jpg", "png", "jpeg"])

# Check if an image has been uploaded
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Preprocess the image (resize, normalize, etc.)
    processed_image = preprocess_input(image)

    # Make predictions using your skin disease model
    prediction = your_skin_disease_model.predict(processed_image)

    # Display the predicted disease name
    st.write(f"Predicted Disease: {prediction}")