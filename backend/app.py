from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define your routes and corresponding functions
@app.route('/')
def home():
    return 'Welcome to the SonicSense backend!'

@app.route('/predictions')
def get_predictions():
    # Placeholder for fetching predictions from your model
    predictions = {
        "gender": "male",
        "age": "30s",
        "language": "english"
    }
    return '<input type="file" accept="audio/*" id="voiceInput" style="display: none;"><button >Start Voice Recognition</button>'

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

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
