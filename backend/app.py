from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Get the directory path of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
audio_directory = os.path.join(current_directory, 'audio')

# Create the 'audio' directory if it doesn't exist
if not os.path.exists(audio_directory):
    os.makedirs(audio_directory)

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
    username = request.form.get('username')  # Get username from the form data

    # If the user does not select a file, the browser sends an empty file without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file with the provided username as the filename in the 'audio' directory
    filename = os.path.join(audio_directory, f'{username}.wav')  # Custom filename based on username
    file.save(filename)

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)