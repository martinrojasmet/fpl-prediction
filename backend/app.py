from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the mock players data
with open('data/final/formatted_data_gw_23.json', 'r') as f:
    mock_data = json.load(f)

@app.route('/api/mock-players', methods=['GET'])
def get_mock_players():
    return jsonify({"players": mock_data['players']})

@app.route('/api/combined-data', methods=['GET'])
def get_combined_data():
    gw = request.args.get('gw')
    # Implement your logic to fetch combined data based on the game week (gw)
    combined_data = []  # Replace with actual combined data fetching logic
    return jsonify(combined_data)

if __name__ == '__main__':
    app.run(debug=True)
