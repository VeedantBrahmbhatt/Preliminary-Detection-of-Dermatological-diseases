import os
import numpy as np
from flask import Flask, request, render_template, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import folium
import requests
import overpy
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Set the upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Load a pre-trained ResNet50 model
model = tf.keras.models.load_model('DenseNetApproach.h5')

disease_descriptions = {
    'Melanoma (MEL)': 'Melanoma is a type of skin cancer that arises from pigment-producing cells called melanocytes. It is often characterized by irregular moles or dark, asymmetrical growths on the skin.',
    'Melanocytic nevus (NV)': 'A melanocytic nevus, commonly known as a mole, is a benign growth on the skin. Moles are usually small, round, and can vary in color.',
    'Basal cell carcinoma (BCC)': 'Basal cell carcinoma is a common type of skin cancer that typically appears as a small, shiny bump or a red, scaly patch. It rarely spreads to other parts of the body.',
    'Actinic keratosis (AK)': 'Actinic keratosis, also known as solar keratosis, is a pre-cancerous skin condition caused by prolonged sun exposure. It often appears as rough, scaly patches on the skin.',
    'Benign keratosis (BKL)': 'Benign keratosis refers to non-cancerous growths on the skin. These growths can include seborrheic keratosis, which are often brown or black and have a waxy appearance.',
    'Dermatofibroma (DF)': 'Dermatofibroma is a benign skin tumor that usually appears as a small, brownish bump on the skin. It is often firm to the touch and may have a central dimple.',
    'Vascular lesion (VASC)': 'Vascular lesions refer to abnormalities in blood vessels. These can include conditions like hemangiomas and port-wine stains, which are characterized by red or purple discolorations on the skin.',
    'Squamous cell carcinoma (SCC)': 'Squamous cell carcinoma is a type of skin cancer that usually appears as a red, scaly patch or a firm, elevated growth. It can be more aggressive than basal cell carcinoma and may spread to other areas of the body.'
}



# Function to process the uploaded image and make predictions
def predict_image(file_path):
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    predictions = model.predict(img_array)
    print(predictions)
    p=np.argmax(predictions)
    l=['Melanoma (MEL)',
    'Melanocytic nevus (NV)',
    'Basal cell carcinoma (BCC)',
    'Actinic keratosis (AK)',
    'Benign keratosis (BKL)',
    'Dermatofibroma (DF)', 
    'Vascular lesion (VASC)',
   'Squamous cell carcinoma (SCC)']
    decoded_prediction = l[p]
    
    return decoded_prediction

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file extension'})
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the uploaded image and make predictions
        prediction = [predict_image(file_path),disease_descriptions[predict_image(file_path)]]

        return render_template('ret.html', data=prediction)

    return render_template('index.html')
@app.route('/try', methods=['GET', 'POST'])
def tryh():
    return render_template("try.html")

@app.route("/getdoc",methods=['GET', 'POST'])
def display_map():
    # User's location (for example, New York)
    try:

        user_lat = float(request.form['latitude'])
        user_lon = float(request.form['longitude'])
        print(user_lat,user_lon)
        # Initialize the Overpass API client
        api = overpy.Overpass()

        # Define a bounding box for the user's location (adjust as needed)
        bounding_box = (
            user_lat - 1, user_lon - 1,
            user_lat + 1, user_lon + 1
        )
        # ['healthcare:speciality'='dermatology']
        query = (
            f"node['amenity'='doctors']"
            f"({bounding_box[0]}, {bounding_box[1]}, {bounding_box[2]}, {bounding_box[3]});"
            f"out;"
        )
        result = api.query(query)
            # Extract doctor data (latitude, longitude, and additional details)
        nearest_doctors = []
        for node in result.nodes:
            lat = float(node.lat)
            lon = float(node.lon)
            name = node.tags.get("name", "Doctor Name Unknown")  # Get the doctor's name, or use a default if not available
            address = node.tags.get("addr:street", "Address Unknown")  # Get the address, or use a default if not available
            phone = node.tags.get("contact:phone", "Phone Unknown")  # Get the phone number, or use a default if not available
            name = name.replace("'", " ")
            address = address.replace("'", " ")
            phone = phone.replace("'", " ")
            doctor_info = {
                "lat": lat,
                "lon": lon,
                "name": name,
                "address": address,
                "phone": phone
            }
            nearest_doctors.append(doctor_info)
        print(nearest_doctors)
            # Create a map centered around the user's location
        m = folium.Map(location=[user_lat, user_lon], zoom_start=12)
        print("reached here")
        for doctor in nearest_doctors:
            popup_content = f"<b>Name:</b> {doctor['name']}<br><b>Address:</b> {doctor['address']}<br><b>Phone:</b> {doctor['phone']}"
            folium.Marker([doctor['lat'], doctor['lon']], popup=popup_content).add_to(m)
        nearest_doctors_json = json.dumps(nearest_doctors, ensure_ascii=False)

            # Create a map centered around the user's location
        m = folium.Map(location=[user_lat, user_lon], zoom_start=12)
        print("reached here")
        return render_template('map.html', nearest_doctors_json=nearest_doctors_json,user_lat=user_lat,user_lon=user_lon, map=m._repr_html_())
    except Exception as e:
        print("errr")
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
