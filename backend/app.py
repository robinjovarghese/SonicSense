from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all origins

# Define your routes and corresponding functions
@app.route('/')
def home():
    return 'Welcome to the SonicSense backend!'

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has the file part
    if 'voiceFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['voiceFile']
    
    # If the user does not select a file, the browser sends an empty file without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to a specified location
    file.save('audio/frontendvoice.wav')  # Replace '/path/to/save/' with the desired save path

    # Now call your main program
    result = subprocess.run(['python3', 'main.py'], capture_output=True, text=True)
    
    # Print the result for testing
    print("Result from main.py:", result.stdout)

    # Extract the JSON array from the output string
    json_array_str = result.stdout.split('\n')[-2]  # Assuming the JSON array is always the second-to-last line
    json_array = json.loads(json_array_str)

    # Return the JSON array to the frontend
    return jsonify(json_array), 200

if __name__ == '__main__':
    # Run the app on custom port 7250
    app.run(debug=True, port=7250)
