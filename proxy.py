from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
import requests
app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

@app.route('/')
def search_hospitals():
    # MapmyIndia API endpoint
    api_url = 'https://atlas.mapmyindia.com/api/places/search/json'
    
    # Parameters
    query = request.args.get('query')
    location = request.args.get('location')
    api_key = '40fc61ae97e3e151928817751d0acb89'  # Replace with your MapmyIndia API key

    # Construct the MapmyIndia API request
    params = {
        'query': query,
        'location': location,
        'api_key': api_key
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Return the JSON response from MapmyIndia to the client
        return jsonify(response.json())

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(port=5000)
