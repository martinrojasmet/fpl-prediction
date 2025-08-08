import pandas as pd
import requests
import os
import json

URL = "http://localhost:3000/api"

# Get Dataframes
current_directory = os.getcwd()

players = pd.read_csv(f"{current_directory}/backend/data/pivot/players.csv")
teams = pd.read_csv(f"{current_directory}/backend/data/pivot/teams.csv")
positions = pd.read_csv(f"{current_directory}/backend/data/pivot/positions.csv")
games = pd.read_csv(f"{current_directory}/backend/data/final/understat_games.csv")

fixtures = pd.read_csv(f"{current_directory}/backend/data/final/2425_players_data.csv")
predictions = pd.read_csv(f"{current_directory}/backend/data/final/predictions.csv")

double_gw = pd.DataFrame()
with open(f"{current_directory}/backend/utils/double_gw.json", "r") as f:
    double_gw_json = json.load(f)

    for key, item in double_gw_json.items():
        row = {
            "home": item["home"],
            "away": item["away"],
            "gw": int(key),
            "original_gw": item["original_gw"],
            "understat_id": item["understat_id"],
            "season": "2024-25"
        }

        double_gw = double_gw._append(row, ignore_index=True)

# Data conversion
players = players.rename(columns={"fpl": "fpl_name", "understat": "understat_name", "fpl_2024-25": "fpl_202425"})

# Upload data
# fields_list = []
for _, row in fixtures.iterrows():
    dict = {col: (row[col] if pd.notna(row[col]) else None) for col in fixtures.columns}

    # Convert datetime columns to ISO format with UTC 'Z'
    for dt_col in ["understat_date", "fpl_kickoff_time"]:
        if dt_col in dict and dict[dt_col] is not None:
            try:
                dt = pd.to_datetime(dict[dt_col], utc=True)
                dict[dt_col] = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            except Exception:
                pass
    
    # if dict.get("understat_team") is None:
    #     dict["understat_team"] = ""

    data = {"fixtures": [dict]}

    # print(data)

    response = requests.post(f"{URL}/fixtures", json=data)

    if response.status_code != 201:
        # print(f"Prediction for {row['player_name']} not created")
        print(response.status_code)
        print(response.text)