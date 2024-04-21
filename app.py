from flask import Flask, jsonify

app = Flask(__name__)

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
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
