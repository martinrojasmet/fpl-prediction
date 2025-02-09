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
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from datetime import datetime
import random

fpl_data = pd.read_csv('./data/final/2425_players_data.csv')
team_data = pd.read_csv('./data/pivot/teams.csv')
next_games_path = './utils/next_games.json'
predictions_path = './data/final/predictions.csv'
url = "https://fantasy.premierleague.com/api/fixtures/"
load_dotenv()
season = os.getenv('SEASON')
start_date = os.getenv('START_DATE')
players_df = pd.read_csv('./data/pivot/players.csv')

predictions_path = './data/final/predictions.csv'
teams_path = './data/pivot/teams.csv'
players_path = './data/final/2425_players_data.csv'

img_api_url = "http://localhost:5000/api/assets/players/"
player_images_folder_path = "/home/martin/Documents/GitHub/fpl/backend/assets/player_images/"
default_player_image_path = img_api_url + "default.png"

point_predictions_json_folder = "/home/martin/Documents/GitHub/fpl-prediction/backend/data/final/point_prediction_jsons/"
game_predictions_json_folder = "/home/martin/Documents/GitHub/fpl-prediction/backend/data/final/game_prediction_jsons/"

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

def get_gws_predicted_jsons(type_data):
    gws = []

    if type_data == "players":
        json_folder = point_predictions_json_folder
    else:
        json_folder = game_predictions_json_folder

    for filename in os.listdir(json_folder):
        name = filename.split('.')[0]
        if name.isdigit():
            gws.append(int(name))

    return gws

def prediction(gw):
    if gw != 38:
        get_next_games(gw)

        next_gw = gw + 1
        point_prediction(fpl_data, team_data, next_gw)

        gw_prediction_to_json(next_gw)

        game_prediction(next_gw)

def game_prediction(gw):
    understat_game_df = pd.read_csv("./data/tmp/understat_game.csv")
    understat_player_df = pd.read_csv("./data/tmp/understat_player.csv")
    teams_df = pd.read_csv("./data/pivot/teams.csv")
    players_2425_df = pd.read_csv("./data/final/2425_players_data.csv")
    final_understat_game_df = pd.read_csv("./data/final/understat_games.csv")

    gw_already = ((final_understat_game_df['gw'] == (gw-1)) & (final_understat_game_df['date'] > start_date)).any()

    with open('./utils/next_games.json', 'r') as f:
        next_games_json = json.load(f)

    games_df = pd.DataFrame()

    if not gw_already:
        # Add Understat scraped data

        game_columns = understat_game_df.columns.tolist()

        home_columns = game_columns.copy()
        home_columns.remove("away")
        away_columns = game_columns.copy()
        away_columns.remove("home")

        gw_df = players_2425_df[["gw", "local_understat_fixture"]]
        gw_df = gw_df.rename(columns={"local_understat_fixture": "id"})
        gw_df = gw_df.drop_duplicates()

        understat_game_df = understat_game_df.merge(gw_df, on=["id"], how="left")

        home_columns.append("gw")

        home_df = understat_game_df[home_columns].rename(columns={'home': 'team'})
        away_df = understat_game_df[away_columns].rename(columns={'away': 'team'})

        home_df["is_home"] = True
        away_df["is_home"] = False

        new_understat_game_df = pd.concat([home_df, away_df], ignore_index=True)

        player_agg = understat_player_df.groupby(['game_id', 'team_name']).agg({
            'goals': 'sum',
            'xG': 'sum',
            'assists': 'sum',
            'xA': 'sum'
        }).reset_index().rename(columns={
            'game_id': 'id',
            'team_name': 'team'
        })

        new_understat_game_df = new_understat_game_df.merge(
            player_agg,
            on=['id', 'team'],
            how='left'
        )
        games_df = pd.concat([games_df, new_understat_game_df], ignore_index=True)
    else:
        print("not")

    # Add next gameweek
    new_gw = []
    for game in next_games_json:
        rand_num = random.randint(3_000_001, 5_000_000)
        data_home = {
            "id": rand_num,
            "understat_id": rand_num,
            "date": datetime.strptime(game["fpl_kickoff_time"], "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d'),
            "team": teams_df.loc[teams_df["definite_team_number"] == game["home_team"], "understat_name"].values[0],
            "gw": gw,
            "is_home": True
        }
        new_gw.append(data_home)

        data_away = {
            "id": rand_num,
            "understat_id": rand_num,
            "date": datetime.strptime(game["fpl_kickoff_time"], "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d'),
            "team": teams_df.loc[teams_df["definite_team_number"] == game["away_team"], "understat_name"].values[0],
            "gw": gw,
            "is_home": False
        }
        new_gw.append(data_away)

    new_gw_df = pd.DataFrame(new_gw)

    games_df = pd.concat([games_df, new_gw_df], ignore_index=True)

    # Previous gameweeks
    common_cols = ["id", "understat_id", "date", "gw"]

    home_cols = common_cols + [col for col in final_understat_game_df.columns if "home" in col and "rolling" not in col and "code" not in col]
    away_cols = common_cols + [col for col in final_understat_game_df.columns if "away" in col and "rolling" not in col and "code" not in col]

    prev_home_df = final_understat_game_df[home_cols].copy()
    prev_away_df = final_understat_game_df[away_cols].copy()

    prev_home_df = prev_home_df.rename(columns=lambda x: x.replace("home_", "").replace("_", "") if x not in common_cols else x)
    prev_away_df = prev_away_df.rename(columns=lambda x: x.replace("away_", "").replace("_", "") if x not in common_cols else x)

    prev_home_df = prev_home_df.rename(columns={"home": "team"})
    prev_away_df = prev_away_df.rename(columns={"away": "team"})

    prev_home_df["is_home"] = True
    prev_away_df["is_home"] = False

    prev_gw = pd.DataFrame()

    prev_gw = pd.concat([prev_gw, prev_home_df], ignore_index=True)
    prev_gw = pd.concat([prev_gw, prev_away_df], ignore_index=True)

    games_df = pd.concat([games_df, prev_gw], ignore_index=True)

    # Add rolling values
    games_df = games_df.sort_values(['team', 'date'])

    metrics = ['goals', 'xG', 'assists', 'xA']

    for metric in metrics:
        games_df[f'rolling_{metric}'] = (
            games_df.groupby('team')[metric]
            .rolling(window=5, min_periods=1)
            .mean()
            .groupby('team')
            .shift(1)
            .reset_index(level=0, drop=True)
        )
        games_df.loc[games_df[f'rolling_{metric}'].isna(), f'rolling_{metric}'] = 0

        games_df[f'rolling_{metric}'] = games_df[f'rolling_{metric}'].round(2)
        if not np.issubdtype(games_df[metric].dtype, np.integer):
            games_df[metric] = games_df[metric].round(2)

    # Merge home and away data
    home_df = games_df[games_df["is_home"] == True].copy()
    away_df = games_df[games_df["is_home"] == False].copy()

    for metric in metrics:
        home_df = home_df.rename(columns={metric: f"home_{metric}", f"rolling_{metric}": f"rolling_home_{metric}", "team": "home"})
        away_df = away_df.rename(columns={metric: f"away_{metric}", f"rolling_{metric}": f"rolling_away_{metric}", "team": "away"})

    home_df.drop('is_home', axis=1, inplace=True)
    away_df.drop('is_home', axis=1, inplace=True)

    teams_numbers_df = teams_df[["definite_team_number","understat_name"]]
    teams_numbers_df = teams_numbers_df.drop_duplicates()

    home_df = home_df.merge(teams_numbers_df, left_on=["home"], right_on=["understat_name"], how="left")
    home_df.drop('understat_name', axis=1, inplace=True)
    home_df = home_df.rename(columns={"definite_team_number": "home_team_code"})

    away_df = away_df.merge(teams_numbers_df, left_on=["away"], right_on=["understat_name"], how="left")
    away_df.drop('understat_name', axis=1, inplace=True)
    away_df = away_df.rename(columns={"definite_team_number": "away_team_code"})

    away_columns = list(away_df.columns)
    away_columns.remove("gw")
    away_df = away_df[away_columns]

    result_df = home_df.merge(
        away_df,
        on=['id', 'understat_id', 'date'],
        how='left'
    )

    conditions = [
        result_df["home_goals"].isna() & result_df["away_goals"].isna(),
        result_df["home_goals"] == result_df["away_goals"],
        result_df["home_goals"] > result_df["away_goals"],
        result_df["home_goals"] < result_df["away_goals"]
    ]

    values = [
        np.nan,
        0,
        1,
        2
    ]
    result_df["result"] = np.select(conditions, values, default=-1)
    result_df = result_df.sort_values("date")
    result_df["gw"] = result_df["gw"].astype(int)

    result_not_pred = result_df[(result_df["gw"] != gw) | (result_df["date"] <= start_date)]

    if not gw_already:
        # Save
        result_not_pred.to_csv("./data/final/understat_games.csv", index=False)
        print("saved")

    # Prediction
    xgb = XGBClassifier(n_estimators=50, random_state=10)

    test = result_df[(result_df["gw"] == gw) & (result_df["date"] >= start_date)]
    train = result_df[~result_df.index.isin(test.index)]

    normal_predictors = ['home_team_code', 'away_team_code']

    predictors = ['home_xG', 'away_xG', 'home_xA', 'away_xA', 'home_goals', 'away_goals', 'home_assists', 'away_assists']
    rolling_predictors = ['rolling_home_xG', 'rolling_away_xG', 'rolling_home_xA', 'rolling_away_xA', 'rolling_home_goals', 'rolling_away_goals', 'rolling_home_assists', 'rolling_away_assists']
    train_predictors = normal_predictors + predictors
    test_predictors = normal_predictors + predictors

    xgb.fit(train[train_predictors], train['result'])
    test.drop(columns=predictors, inplace=True)

    for word in rolling_predictors:
        test.rename(columns={word: word[8:]}, inplace=True)

    preds = xgb.predict(test[test_predictors])

    output = [
        {"home_team_code": home, "away_team_code": away, "result": int(result)}
        for home, away, result in zip(test["home"], test["away"], preds)
    ]

    json_output = json.dumps(output, indent=4)
    with open(f"./data/final/game_prediction_jsons/{gw}.json", "w") as file:
        file.write(json_output)
