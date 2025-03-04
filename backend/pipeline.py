import requests
import pandas as pd
from scraper import scrape_understat_data
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# PIVOT paths
pivot_folder_path = "./data/pivot/"
players_pivot_path = pivot_folder_path + "players.csv"
positions_pivot_path = pivot_folder_path + "positions.csv"
teams_pivot_path = pivot_folder_path + "teams.csv"

# PIVOT df
teams_pivot_df = pd.read_csv(teams_pivot_path)
players_df = pd.read_csv(players_pivot_path)
positions_df = pd.read_csv(positions_pivot_path)

# TMP paths
tmp_folder_path = "./data/tmp/"
understat_game_path = tmp_folder_path + "understat_game.csv"
understat_player_path = tmp_folder_path + "understat_player.csv"
understat_merged_path = tmp_folder_path + "understat_merged.csv"
fpl_player_path = tmp_folder_path + "fpl_player.csv"
result_path = tmp_folder_path + "result.csv"

# TMP df
new_understat_player_df = pd.read_csv(understat_player_path)
new_understat_game_df = pd.read_csv(understat_game_path)

# 2425
final_folder_path = "./data/final/"
players_2425_path = final_folder_path + "2425_players_data.csv"
players_2425_df = pd.read_csv(players_2425_path)

# variables
start_date_season = os.getenv('START_DATE')
gw = int(os.getenv('GW'))
# last_gw = int(os.getenv('GW'))

# logging
logging_folder_path = "/home/martin/Documents/GitHub/fpl-prediction/backend/utils/"
logging.basicConfig(filename=f'{logging_folder_path}pipeline.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# not used
def unique_players(players_df):
    players_fpl_id_list = players_df["fpl_2024-25"].to_list()
    unique_rows = players_df.drop_duplicates(subset=["fpl", "fpl_2024-25"])

    if len(unique_rows) == len(players_df):
        print("No repeated name-id pairs found.")
        return True
    else:
        print("Repeated name-id pairs found.")
        duplicated_rows = players_df[players_df.duplicated(subset=["fpl", "fpl_2024-25"], keep=False)]
        print(duplicated_rows[["fpl_2024-25", "fpl"]])
        return False

def add_fpl_name_data(players_df):
    response = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    fpl_data = response.json()

    players_fpl_name_list = players_df["fpl"].to_list()
    players_fpl_id_list = players_df["fpl_2024-25"].to_list()

    name_list = []
    for element in fpl_data["elements"]:
        name = element["first_name"] + " " + element["second_name"]
        fpl_id = element["id"]
        opta_id = element["photo"].split(".")[0]
        if (name not in players_fpl_name_list) or (fpl_id not in players_fpl_id_list):
            new_row = {"fpl": name, "fpl_2024-25": fpl_id, "opta_id": opta_id}
            players_df = players_df._append(new_row, ignore_index=True)
            print("Nuevo jugador encontrado: ", name, fpl_id)

    if unique_players(players_df):
        players_df.to_csv(players_pivot_path, index=False)

def merge_understat_data(understat_player_df, understat_game_df):
    merged_df = pd.merge(understat_player_df, understat_game_df, left_on="game_id", right_on="id", how="inner")
    merged_df = merged_df.drop(columns=["home", "id_y"])
    merged_df = merged_df.rename(columns={"id_x": "player_game_id", "understat_id": "understat_game_id"})
    merged_df.to_csv(understat_merged_path, index=False)

def add_understat_name_data(understat_merged_df, players_df):
    understat_merged_df["date"] = pd.to_datetime(understat_merged_df["date"])
    unique_player_names = understat_merged_df[understat_merged_df["date"] >= start_date_season]["player_name"].unique()
    understat_player_names = understat_merged_df["player_name"].unique()

    lis = []
    for name in unique_player_names:
        if name not in players_df["understat"].values:
            if (players_df["fpl"] == name).any():
                print(f"{name} understat value updated")
                players_df.loc[players_df["fpl"] == name, "understat"] = name
            else:
                lis.append(name)

    players_df.to_csv(players_pivot_path, index=False)

    if lis:
        print("Amount of players out: ", len(lis))
        print(lis)
        raise ValueError("Some players are missing from the players_df.")

def get_fpl_data():
    result_df = pd.DataFrame()

    basic_response = requests.get(f'https://fantasy.premierleague.com/api/bootstrap-static/')
    basic_data = basic_response.json()
    basic_elements = basic_data["elements"]

    for player_index in players_df["fpl_2024-25"].unique():
        basic_element = next((item for item in basic_elements if item["id"] == player_index), None)
        element_response = requests.get(f'https://fantasy.premierleague.com/api/element-summary/{str(int(player_index))}/')
        element_data = element_response.json()
        element_history = element_data["history"]
        for element in element_history:
            if element["round"] >= gw:
                row = {
                    "fpl_name": players_df.loc[players_df["fpl_2024-25"] == player_index, "fpl"].values[0],
                    "position": basic_element["element_type"],
                    "fpl_team": teams_pivot_df.loc[(teams_pivot_df['team'] == basic_element["team"]) & (teams_pivot_df['season'] == "2024-25"), "definite_team_number"].values[0],
                    "assists": element["assists"],
                    "bonus": element["bonus"],
                    "clean_sheets": element["clean_sheets"],
                    "fpl_element": element["element"],
                    "goals_conceded": element["goals_conceded"],
                    "goals_scored": element["goals_scored"],
                    "fpl_kickoff_time": element["kickoff_time"],
                    "minutes": element["minutes"],
                    "opponent_fpl_team_number": teams_pivot_df.loc[(teams_pivot_df['team'] == element["opponent_team"]) & (teams_pivot_df['season'] == "2024-25"), "definite_team_number"].values[0],
                    "own_goals": element["own_goals"],
                    "penalties_missed": element["penalties_missed"],
                    "penalties_saved": element["penalties_saved"],
                    "red_cards": element["red_cards"],
                    "saves": element["saves"],
                    "team_a_score": element["team_a_score"],
                    "team_h_score": element["team_h_score"],
                    "points": element["total_points"],
                    "value": element["value"],
                    "was_home": element["was_home"],
                    "yellow_cards": element["yellow_cards"],
                    "gw": element["round"],
                    "season": "2024-25",
                    "expected_assists": element["expected_assists"],
                    "expected_goals": element["expected_goals"],
                    "bps": element["bps"],
                    "creativity": element["creativity"],
                    "fixture": element["fixture"],
                    "ict_index": element["ict_index"],
                    "influence": element["influence"],
                    "round": element["round"],
                    "selected": element["selected"],
                    "threat": element["threat"],
                    "transfers_balance": element["transfers_balance"],
                    "transfers_in": element["transfers_in"],
                    "transfers_out": element["transfers_out"],
                    "expected_goal_involvements": element["expected_goal_involvements"],
                    "expected_goals_conceded": element["expected_goals_conceded"],
                    "starts": element["starts"]
                }
                result_df = result_df._append(row, ignore_index=True)

    result_df["fpl_date"] = pd.to_datetime(result_df["fpl_kickoff_time"]).dt.strftime('%Y-%m-%d')

    result_df.to_csv(fpl_player_path, index=False)

# not used
def add_iso_data_fpl():
    fpl_player_df["fpl_date"] = pd.to_datetime(fpl_player_df["fpl_kickoff_time"]).dt.strftime('%Y-%m-%d')
    fpl_player_df.to_csv(fpl_player_path, index=False)

# temp
def temp_change_2425(): # Cambiar a 2024-25
    understat_1 = pd.read_csv("understat_merged2.csv")
    players_2425_df["position_number"] = players_2425_df["position"].map(positions_df.set_index("position")["position_number"])
    
    players_2425_df.drop(columns=["opponent_team_name", "fpl_team", "position"], inplace=True)
    players_2425_df.rename(columns={"opponent_team": "fpl_team_number", "position_number": "position"}, inplace=True)

    list_index = []
    for index, row in players_2425_df.iterrows():
        player_game_values = understat_1.loc[(understat_1["date"] == row["understat_date"]) & (understat_1["player_name"] == row["understat_name"]), "player_game_id"].values
        game_values = understat_1.loc[(understat_1["date"] == row["understat_date"]) & (understat_1["player_name"] == row["understat_name"]), "game_id"].values
        minutes = row["minutes"]
        if len(player_game_values) > 0 and len(game_values) > 0:
            players_2425_df.at[index, "local_understat_fixture2"] = game_values[0]
            players_2425_df.at[index, "local_understat_id"] = player_game_values[0]
        else:
            if minutes != 0:
                list_index.append(index)
            else:
                players_2425_df.at[index, "local_understat_fixture2"] = pd.NA
                players_2425_df.at[index, "local_understat_id"] = pd.NA

    print(list_index)
    print(len(list_index))

    players_2425_df.drop(columns=["local_understat_fixture"], inplace=True)
    players_2425_df.rename(columns={"local_understat_fixture2": "local_understat_fixture"}, inplace=True)
    players_2425_df.to_csv("2425_players_data3.csv")

def fix_team_number():
    players_2425_df = pd.read_csv("2425_players_data3.csv")
    players_2425_df = players_2425_df.merge(
        teams_pivot_df[['team', 'definite_team_number', 'season']], 
        left_on=['fpl_team_number', 'season'], 
        right_on=['team', 'season'], 
        how='left'
    )
    players_2425_df.rename(columns={'definite_team_number': 'fpl_team_number2'}, inplace=True)
    players_2425_df.drop(columns=['team'], inplace=True)
    players_2425_df.drop(columns=["fpl_team_number"], inplace=True)
    players_2425_df.rename(columns={"fpl_team_number2": "fpl_team_number"}, inplace=True)
    players_2425_df.to_csv("2425_players_data4.csv", index=False)

def fix_format():
    p2425_df = pd.read_csv("2425_players_data4.csv")
    p2425_df.drop(columns=["Unnamed: 0"], inplace=True)
    columns_order = [
        "season", "gw", "fpl_element", "local_understat_id", "local_understat_fixture",
        "fpl_name", "understat_name", "position", "fpl_team_number", "understat_team", "fpl_kickoff_time", 
        "understat_date", "value", "points", 
        "minutes", "goals_scored", "xG", "goals_conceded", "assists", "xA", "yellow_cards", 
        "red_cards", "clean_sheets", "key_passes", "own_goals", "penalties_missed", 
        "penalties_saved", "saves", "bonus", "team_a_score", "team_h_score", "was_home", 
        "expected_assists", "expected_goals"
    ]
    p2425_df = p2425_df[columns_order]
    p2425_df.to_csv("2425_players_data5.csv", index=False)

def delete_understat_players():
    players_df.drop(columns=["understat_2024-25"], inplace=True)
    players_df.to_csv(players_pivot_path, index=False)
    print(players_df)

def get_understat_names():
    list_numbers = list(teams_pivot_df["definite_team_number"].unique())
    for team_number in teams_pivot_df["definite_team_number"]:
        value = teams_pivot_df[(teams_pivot_df["definite_team_number"] == team_number) & (teams_pivot_df["understat_name"].notna())]["definite_team_number"].values
        if any(val in list_numbers for val in value):
            list_numbers.remove(value[0])

    print(list_numbers)
        
def add_understat_names():
    list_numbers = list(teams_pivot_df["definite_team_number"].unique())
    for team_number in list_numbers:
        value = teams_pivot_df[(teams_pivot_df["definite_team_number"] == team_number) & (teams_pivot_df["understat_name"].notna())]["understat_name"].values[0]
        if pd.isna(teams_pivot_df.loc[teams_pivot_df["definite_team_number"] == team_number, "understat_name"]).any():
            teams_pivot_df.loc[teams_pivot_df["definite_team_number"] == team_number, "understat_name"] = value

    teams_pivot_df.to_csv("./data/pivot/teams2.csv")

def get_list_players_no_team():

    for index, row in players_2425_df.iterrows():
        if row["understat_team"] == "-":
            if row["understat_name"] == 'Kieran Trippier':
                if pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2022-01-07").date():
                    players_2425_df.at[row.name, "understat_team"] = "Newcastle United"
                else:
                    players_2425_df.at[row.name, "understat_team"] = "Tottenham"
            elif row["understat_name"] == 'Kurt Zouma':
                if pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2021-08-27").date():
                    players_2425_df.at[row.name, "understat_team"] = "West Ham"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2019-05-31").date():
                    players_2425_df.at[row.name, "understat_team"] = "Chelsea"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2018-08-09").date():
                    players_2425_df.at[row.name, "understat_team"] = "Everton"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2018-05-31").date():
                    players_2425_df.at[row.name, "understat_team"] = "Chelsea"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2017-07-21").date():
                    players_2425_df.at[row.name, "understat_team"] = "Stoke"
                else:
                    players_2425_df.at[row.name, "understat_team"] = "Chelsea"
            elif row["understat_name"] == 'Reiss Nelson':
                if pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2025-06-30").date():
                    players_2425_df.at[row.name, "understat_team"] = "Arsenal"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2024-08-30").date():
                    players_2425_df.at[row.name, "understat_team"] = "Fulham"
                else:
                    players_2425_df.at[row.name, "understat_team"] = "Arsenal"
            elif row["understat_name"] == 'Harvey Elliott':
                 players_2425_df.at[row.name, "understat_team"] = "Liverpool"
            elif row["understat_name"] == 'Oleksandr Zinchenko':
                if pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2022-07-22").date():
                    players_2425_df.at[row.name, "understat_team"] = "Arsenal"
                else:
                    players_2425_df.at[row.name, "understat_team"] = "Manchester City"
            elif row["understat_name"] == 'Mario Lemina':
                if pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2023-01-13").date():
                    players_2425_df.at[row.name, "understat_team"] = "Wolverhampton Wanderers"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2021-05-31").date():
                    players_2425_df.at[row.name, "understat_team"] = "Southampton"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2020-08-30").date():
                    players_2425_df.at[row.name, "understat_team"] = "Fulham"
                else:
                    players_2425_df.at[row.name, "understat_team"] = "Southhampton"
            elif row["understat_name"] == 'Ashley Young':
                if pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2023-07-13").date():
                    players_2425_df.at[row.name, "understat_team"] = "Everton"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2021-07-01").date():
                    players_2425_df.at[row.name, "understat_team"] = "Aston Villa"
                else:
                    players_2425_df.at[row.name, "understat_team"] = "Manchester United"
            elif row["understat_name"] == 'Konstantinos Mavropanos':
                if pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2023-08-22").date():
                    players_2425_df.at[row.name, "understat_team"] = "West Ham"
                else:
                    players_2425_df.at[row.name, "understat_team"] = "Arsenal"
            elif row["understat_name"] == 'George Hirst':
                if pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2023-07-13").date():
                    players_2425_df.at[row.name, "understat_team"] = "Ipswich"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2023-05-31").date():
                    players_2425_df.at[row.name, "understat_team"] = "Leicester"
                elif pd.to_datetime(row["fpl_kickoff_time"]).date() >= pd.to_datetime("2023-01-08").date():
                    players_2425_df.at[row.name, "understat_team"] = "Ipswich"
                else:
                    players_2425_df.at[row.name, "understat_team"] = "Leicester"

    players_2425_df.to_csv("2425_players_data2.csv", index=False)

def get_team_name():
    players_2425_df["understat_team"] = players_2425_df["understat_team"].replace("Southhampton", "Southampton")

    fpl_raw_data = pd.read_csv("fpl_raw_data.csv")[["name", "kickoff_time", 'team']]
    fpl_raw_data["name"] = fpl_raw_data["name"].str.replace("_", ' ', regex=True)
    fpl_raw_data["team"] = fpl_raw_data["team"].str.replace(r'\d+', '', regex=True)
    fpl_raw_data["team"] = fpl_raw_data["team"].str.rstrip()

    merged_df = pd.merge(players_2425_df, fpl_raw_data, left_on=["fpl_name", "fpl_kickoff_time"], right_on=["name", "kickoff_time"], how="left")
    merged_df = merged_df.drop(columns=["name", "kickoff_time"])
    merged_df = merged_df.rename(columns={'team': 'fpl_team'})

    matched_rows = merged_df[merged_df["fpl_team"].notna()]
    unmatched_rows = merged_df[merged_df["fpl_team"].isna()]

    unmatched_rows["fpl_team"] = unmatched_rows.apply(
        lambda row: teams_pivot_df.loc[teams_pivot_df["understat_name"] == row["understat_team"], "team_name"].values[0] 
        if row["understat_team"] in teams_pivot_df["understat_name"].values else row["fpl_team"], axis=1
    )

    matched_rows = matched_rows._append(unmatched_rows[unmatched_rows["fpl_team"].notna()])
    unmatched_rows = unmatched_rows[unmatched_rows["fpl_team"].isna()]

    print(f"Number of matched rows: {len(matched_rows)}")
    print(f"Number of unmatched rows: {len(unmatched_rows)}")

    matched_rows = matched_rows.merge(
        teams_pivot_df[['team_name', 'definite_team_number']], 
        left_on='fpl_team', 
        right_on='team_name', 
        how='left'
    )
    matched_rows.drop(columns=['fpl_team', 'team_name'], inplace=True)
    matched_rows.rename(columns={'definite_team_number': 'fpl_team'}, inplace=True)

    count_no_team_number = matched_rows["fpl_team"].isna().sum()
    print(f"Number of players without a definite_team_number: {count_no_team_number}")

    columns_order = [
        "season", "gw", "fpl_element", "local_understat_id", "local_understat_fixture", "fpl_name", 
        "understat_name", "position", "fpl_team", "understat_team", "opponent_fpl_team_number", "fpl_kickoff_time", 
        "understat_date", "value", "points", "minutes", "goals_scored", "xG", "goals_conceded", "assists", 
        "xA", "yellow_cards", "red_cards", "clean_sheets", "key_passes", "own_goals", "penalties_missed", 
        "penalties_saved", "saves", "bonus", "team_a_score", "team_h_score", "was_home", "expected_assists", 
        "expected_goals"
    ]
    matched_rows = matched_rows[columns_order]
    matched_rows["fpl_team"] = matched_rows["fpl_team"].astype(int)
    matched_rows = matched_rows.sort_values(by=["fpl_kickoff_time", "fpl_name"])
    matched_rows.to_csv("2425_players_data2.csv", index=False)

# final
def merge_understat_fpl(fpl_player_df, new_understat_merged_df):
    # Joe Ayodele-Aribo,Joe Ayodele-Aribo,452.0
    # Joe Ayodele-Aribo,Joe Aribo,452.0
    fpl_player_df["understat_fpl_name"] = fpl_player_df["fpl_name"].map(players_df.set_index("fpl")["understat"])

    fpl_player_df["fpl_date"] = pd.to_datetime(fpl_player_df["fpl_date"]).dt.strftime('%Y-%m-%d')
    new_understat_merged_df["date"] = pd.to_datetime(new_understat_merged_df["date"]).dt.strftime('%Y-%m-%d')
    result_df = fpl_player_df.merge(new_understat_merged_df, left_on=["understat_fpl_name", "fpl_date"], right_on=["player_name", "date"], how="left")

    # duplicated = result_df[(result_df["fpl_name"].notna()) & (result_df["game_id"].notna())]
    # duplicated = duplicated[duplicated.duplicated(subset=["fpl_name", "game_id"], keep=False)]
    # print(duplicated[["fpl_name", "game_id"]])

    result_df = result_df[result_df["fpl_name"].notna()]

    unmatched_fpl_rows = result_df[result_df["player_game_id"].isna()]
    matched_fpl_rows = result_df[result_df["player_game_id"].notna()]
    print(f"Number of matched fpl rows: {len(matched_fpl_rows)}")
    print(f"Number of unmatched fpl rows: {len(unmatched_fpl_rows)}")

    matched_understat_rows = new_understat_merged_df[new_understat_merged_df["player_game_id"].isin(matched_fpl_rows["player_game_id"])]
    unmatched_understat_rows = new_understat_merged_df[~new_understat_merged_df["player_game_id"].isin(matched_fpl_rows["player_game_id"])]
    print(f"Number of matched understat rows: {len(matched_understat_rows)}")
    print(f"Number of unmatched understat rows: {len(unmatched_understat_rows)}")

    if len(unmatched_understat_rows) > 0:
        print("ALERTA DATOS NO ENCONTRADOS")
        print(unmatched_understat_rows)
        unmatched_fpl_rows.to_csv("", index=False)
        raise ValueError("There are unmatched rows in the understat data.")
    else:
        result_df.rename(columns={"player_game_id": "local_understat_id", "game_id": "local_understat_fixture", "understat_fpl_name":"understat_name",
        "team_name": "understat_team", "date": "understat_date", "minutes_x": "minutes", "assists_x": "assists"}, inplace=True)
        columns_order = [
            "season", "gw", "fpl_element", "local_understat_id", "local_understat_fixture", "fpl_name", 
            "understat_name", "position", "fpl_team", "understat_team", "opponent_fpl_team_number", "fpl_kickoff_time", 
            "understat_date", "value", "points", "minutes", "goals_scored", "xG", "goals_conceded", "assists", 
            "xA", "yellow_cards", "red_cards", "clean_sheets", "key_passes", "own_goals", "penalties_missed", 
            "penalties_saved", "saves", "bonus", "team_a_score", "team_h_score", "was_home", "expected_assists", 
            "expected_goals"
        ]
        result_df = result_df[columns_order]

        result_df.loc[(result_df["minutes"] == 0) & (result_df["xG"].isna()), "xG"] = 0
        result_df.loc[(result_df["minutes"] == 0) & (result_df["xA"].isna()), "xA"] = 0
        result_df.loc[(result_df["minutes"] == 0) & (result_df["key_passes"].isna()), "key_passes"] = 0

        result_df.to_csv(result_path, index=False)

def append_current_data(players_2425_df, result_df):
    players_2425_df = players_2425_df._append(result_df, ignore_index=True)
    players_2425_df = players_2425_df.sort_values(by="fpl_kickoff_time")
    players_2425_df.to_csv("2425_players_data.csv", index=False)

def main():
    try:
        logging.info('FPL data pipeline started...')
        print("FPL data pipeline started...")

        print("Scraping Understat data")
        scrape_understat_data()
        new_understat_player_df = pd.read_csv(understat_player_path)
        new_understat_game_df = pd.read_csv(understat_game_path)

        print("Merging Understat data")
        merge_understat_data(new_understat_player_df, new_understat_game_df)
        new_understat_merged_df = pd.read_csv(understat_merged_path)

        print("Adding FPL name data")
        add_fpl_name_data(players_df)

        print("Adding Understat name data")
        add_understat_name_data(new_understat_merged_df, players_df)

        # print("Getting FPL data")
        # get_fpl_data()

        # print("Merging Understat and FPL data")
        # fpl_player_df = pd.read_csv(fpl_player_path)
        # merge_understat_fpl(fpl_player_df, new_understat_merged_df)

        # print("Append new data to 2425")
        # result_df = pd.read_csv(result_path)
        # append_current_data(players_2425_df, result_df)

        # print("FPL data pipeline finished")
        # logging.info('FPL data pipeline finished')
    except Exception as e:
        print(e)
        logging.error(f'Failed to run pipeline: {e}')

main()
