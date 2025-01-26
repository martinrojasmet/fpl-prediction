import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import os
from dotenv import load_dotenv
import requests
import json

fpl_data = pd.read_csv('./data/final/2425_players_data.csv')
team_data = pd.read_csv('./data/pivot/teams.csv')
next_games_path = './utils/next_games.json'
predictions_path = './data/final/predictions.csv'
url = "https://fantasy.premierleague.com/api/fixtures/"
load_dotenv()
season = os.getenv('SEASON')
players_df = pd.read_csv('./data/pivot/players.csv')

predictions_path = './data/final/predictions.csv'
teams_path = './data/pivot/teams.csv'
players_path = './data/final/2425_players_data.csv'

img_api_url = "http://localhost:5000/api/assets/players/"
player_images_folder_path = "/home/martin/Documents/GitHub/fpl/backend/assets/player_images/"
default_player_image_path = img_api_url + "default.png"

point_predictions_json_folder = "/home/martin/Documents/GitHub/fpl/backend/data/final/point_prediction_jsons/"

def point_prediction(fpl_data, team_data, gw):
    if (gw not in get_gws_predicted()):
        fpl_data = fpl_data[['understat_name', 'fpl_team', 'opponent_fpl_team_number', 'points', 'fpl_kickoff_time']]
        understat_names = fpl_data['understat_name'].dropna().unique()


        if os.path.exists(predictions_path):
            predictions = pd.read_csv(predictions_path)
        else:
            predictions = pd.DataFrame(columns=['player_name', 'opponent_team', 'global_predicted_points', 'opponent_predicted_points'])

        for name in understat_names:
            player_data = fpl_data[fpl_data['understat_name'] == name]
            opta_id_values = players_df.loc[players_df['understat'] == name, 'opta_id'].values
            if len(opta_id_values) > 0:
                opta_id = opta_id_values[-1]

            normal_model = LinearRegression()
            team_model = XGBRegressor(enable_categorical=True, learning_rate=0.001, n_estimators=150, random_state=50)

            # All games for the player
            if len(player_data) >= 2:
                player_data.loc[:, 'fpl_kickoff_time'] = pd.to_datetime(player_data['fpl_kickoff_time'])
                player_data = player_data.sort_values('fpl_kickoff_time')

                player_data['ordinal_time'] = player_data['fpl_kickoff_time'].map(pd.Timestamp.toordinal)
                x = player_data[['ordinal_time']]
                y = player_data['points']

                normal_model.fit(x, y)

                last_opponent, last_date = game_for_player(fpl_data[fpl_data['understat_name'] == name]['fpl_team'].values[-1], next_games_path)

                # last_date = player_data['fpl_kickoff_time'].iloc[-1]
                last_date = pd.to_datetime(last_date)
                last_ordinal = last_date.toordinal()
                predicted_points = normal_model.predict(pd.DataFrame([[last_ordinal]], columns=['ordinal_time']))
                # actual_points = player_data['points'].iloc[-1]

                # last_opponent = player_data['opponent_fpl_team_number'].iloc[-1]

                team_filtered_data = fpl_data[(fpl_data['understat_name'] == name) & (fpl_data['opponent_fpl_team_number'] == last_opponent)]

                # Games against the team
                if len(team_filtered_data) >= 2:
                    team_filtered_data.loc[:, 'fpl_kickoff_time'] = pd.to_datetime(team_filtered_data['fpl_kickoff_time'])
                    team_filtered_data = team_filtered_data.sort_values('fpl_kickoff_time')

                    team_filtered_data['ordinal_time'] = team_filtered_data['fpl_kickoff_time'].map(pd.Timestamp.toordinal)
                    x_team = team_filtered_data[['ordinal_time']]
                    y_team = team_filtered_data['points']

                    x_team = x_team.astype(float)
                    team_model.fit(x_team, y_team)

                    # last_date_team = team_filtered_data['fpl_kickoff_time'].iloc[-1]
                    last_ordinal_team = last_ordinal
                    predicted_points_team = team_model.predict(pd.DataFrame([[last_ordinal_team]], columns=['ordinal_time']))

                    row = {
                        # 'fpl_name': fpl_name,
                        'understat_name': name,
                        'opta_id': opta_id,
                        'opponent_team': last_opponent,
                        'gw': gw,
                        'global_predicted_points': predicted_points[0],
                        'opponent_predicted_points': predicted_points_team[0]
                    }
                    predictions = pd.concat([predictions, pd.DataFrame([row])], ignore_index=True)
                else:
                    row = {
                        # 'fpl_name': fpl_name,
                        'understat_name': name,
                        'opta_id': opta_id,
                        'opponent_team': last_opponent,
                        'gw': gw,
                        'global_predicted_points': predicted_points[0],
                        'opponent_predicted_points': -5000
                    }
                    predictions = pd.concat([predictions, pd.DataFrame([row])], ignore_index=True)
            else:
                row = {
                    # 'fpl_name': fpl_name,
                    'understat_name': name,
                    'opta_id': opta_id,
                    'opponent_team': last_opponent,
                    'gw': gw,
                    'global_predicted_points': -5000,
                    'opponent_predicted_points': -5000
                }
                predictions = pd.concat([predictions, pd.DataFrame([row])], ignore_index=True)

        # Revisar
        predictions.loc[predictions['global_predicted_points'] == -5000, 'global_predicted_points'] = 0
        predictions.loc[predictions['opponent_predicted_points'] == -5000, 'opponent_predicted_points'] = 0

        predictions.loc[predictions['global_predicted_points'] < 0, 'global_predicted_points'] = 0
        predictions.loc[predictions['opponent_predicted_points'] < 0, 'opponent_predicted_points'] = 0

        team_percentage = 0.35

        predictions['combined_predicted_points'] = predictions['global_predicted_points']*(1-team_percentage) + predictions['opponent_predicted_points']*team_percentage

        predictions['gw'] = predictions['gw'].astype(int)
        predictions['opta_id'] = predictions['opta_id'].astype(int)
        predictions['global_predicted_points'] = predictions['global_predicted_points'].fillna(0).round(2)
        predictions['opponent_predicted_points'] = predictions['opponent_predicted_points'].fillna(0).round(2)
        predictions['combined_predicted_points'] = predictions['combined_predicted_points'].fillna(0).round(2)
        predictions = predictions[['understat_name', 'opta_id', 'gw', 'opponent_team', 'global_predicted_points', 'opponent_predicted_points', 'combined_predicted_points']]
        predictions.to_csv(predictions_path, index=False)

def get_next_games(current_gw):
    next_gw = current_gw + 1
    response = requests.get(url)
    fixtures = response.json()
 
    result = []
    for fixture in fixtures:
        if fixture['event'] == next_gw:
            home_team = fixture['team_h']
            away_team = fixture['team_a']
            kickoff_time = fixture['kickoff_time']
            home_team_number = int(team_data[(team_data['team'] == home_team) & (team_data['season'] == season)]['definite_team_number'].values[0])
            away_team_number = int(team_data[(team_data['team'] == away_team) & (team_data['season'] == season)]['definite_team_number'].values[0])
            result.append({'home_team': home_team_number, 'away_team': away_team_number, 'fpl_kickoff_time': kickoff_time})
    with open(next_games_path, 'w') as f:
        json.dump(result, f, indent=4)

def game_for_player(team_number, next_games_path):
    kickoff_time = None
    is_home = None
    opponent = None
    with open(next_games_path, 'r') as f:
        games_json = json.load(f)

    for game in games_json:
        home = game["home_team"] == team_number
        away = game["away_team"] == team_number

        if home:
            opponent = game["away_team"]
            kickoff_time = game['fpl_kickoff_time']
        elif away:
            opponent = game["home_team"]
            kickoff_time = game['fpl_kickoff_time']

    return opponent, kickoff_time

def gw_prediction_to_json(gw):
    predictions = pd.read_csv(predictions_path)
    teams = pd.read_csv(teams_path)
    players_data = pd.read_csv(players_path)

    # Filter data for the given gameweek
    predictions_gw = predictions[predictions['gw'] == gw]

    # Format data for frontend
    formatted_data = []
    for _, row in predictions_gw.iterrows():
        opponent_name = teams.loc[teams['definite_team_number'] == row['opponent_team'], 'understat_name'].values[-1]
        previous_points = players_data.loc[players_data['understat_name'] == row['understat_name'], 'points'].tail(5).values
        previous_points = np.pad(previous_points, (5 - len(previous_points), 0), 'constant', constant_values=(0,))

        image_path = player_images_folder_path + str(int(row['opta_id'])) + ".png"
        if os.path.exists(image_path):
            image_path = img_api_url + str(int(row['opta_id'])) + ".png"
        else:
            image_path = default_player_image_path

        if not pd.isna(row['understat_name']) and row['understat_name'] != "":
            formatted_data.append({
                'id': int(row['opta_id']),
                'name': row['understat_name'],
                'imageUrl': image_path, 
                'opponent': opponent_name,
                'expectedPoints': float(row['combined_predicted_points']),
                'previousPoints': list(map(float, previous_points))
            })

        with open(point_predictions_json_folder + str(gw) + '.json', 'w') as f:
            json.dump(formatted_data, f, indent=4)

def get_gws_predicted():
    result = []
    if os.path.exists(predictions_path):
        point_prediction = pd.read_csv(predictions_path)
        result = list(point_prediction["gw"].unique())
    return result

def get_gws_predicted_jsons():
    gws = []

    for filename in os.listdir(point_predictions_json_folder):
        name = filename.split('.')[0]
        if name.isdigit():
            gws.append(int(name))

    return gws

def predicition(gw):
    if gw != 38:
        get_next_games(gw)

        next_gw = gw + 1
        point_prediction(fpl_data, team_data, next_gw)

        gw_prediction_to_json(next_gw)

predicition(22)