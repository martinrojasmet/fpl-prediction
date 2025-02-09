from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import json

from prediction import get_gws_predicted_jsons

point_predictions_json_folder = "/home/martin/Documents/GitHub/fpl-prediction/backend/data/final/point_prediction_jsons/"
game_predictions_json_folder = "/home/martin/Documents/GitHub/fpl-prediction/backend/data/final/game_prediction_jsons/"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve image files
@app.route('/api/assets/players/<path:filename>')
def serve_assets(filename):
    assets_dir = '/home/martin/Documents/GitHub/fpl/backend/assets/player_images/'
    return send_from_directory(assets_dir, filename)

# Get GW point data
@app.route('/api/predictions/points/gws/', methods=['GET'])
def get_gws_predicted():
    gw = request.args.get('gw')

    if not gw:
        return jsonify({"gw_predictions": sorted(get_gws_predicted_jsons("players"))})
    
    if not gw.isdigit():
        return jsonify({"error": "Please provide a valid GW (Game Week) number as a parameter."}), 400

    gw_filename = f"{gw}.json"
    try:
        with open(os.path.join(point_predictions_json_folder, gw_filename), 'r') as file:
            gw_data = json.load(file)
            return jsonify({"players": gw_data})
    except Exception as e:
        return jsonify({"error": f"Failed to load GW {gw} data: {str(e)}"}), 500

# Get GW game data
@app.route('/api/predictions/games/gws/', methods=['GET'])
def get_games_predicted():
    gw = request.args.get('gw')

    if not gw:
        return jsonify({"gw_predictions": sorted(get_gws_predicted_jsons("games"))})
    
    if not gw.isdigit():
        return jsonify({"error": "Please provide a valid GW (Game Week) number as a parameter."}), 400

    gw_filename = f"{gw}.json"
    try:
        with open(os.path.join(game_predictions_json_folder, gw_filename), 'r') as file:
            gw_data = json.load(file)
            return jsonify({"games": gw_data})
    except Exception as e:
        return jsonify({"error": f"Failed to load GW {gw} data: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)