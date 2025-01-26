import re
import os
import datetime
import pandas as pd
from playwright.sync_api import Playwright, sync_playwright, expect

base_url = "https://understat.com/match/"
folder_path = "./data/tmp/"
player_game_df_path = folder_path + "understat_player.csv"
games_df_path = folder_path + "understat_game.csv"
indexes_path = "./utils/scraper_indexes.txt"

def get_actual_value(xNumber):
    number_regex = r"([-+]?\d+\.\d+)"
    match = re.search(number_regex, xNumber)
    return match.group(0)

def get_data_from_players(table, rows, player_game_df, player_game_id, game_id, team_name):
    for index in range(rows.count()):
        row = table.locator("tr").nth(index)

        player_name = row.locator("td").nth(1).inner_text()
        minutes = row.locator("td").nth(3).inner_text()
        shots = row.locator("td").nth(4).inner_text()
        goals = row.locator("td").nth(5).inner_text()
        key_passes = row.locator("td").nth(6).inner_text()
        assists = row.locator("td").nth(7).inner_text()
        xG_td = row.locator("td").nth(8).inner_text()
        xA_td = row.locator("td").nth(9).inner_text()
        xG = get_actual_value(xG_td)
        xA = get_actual_value(xA_td)
        player_game_df = player_game_df._append({
            "id": player_game_id,
            "player_name": player_name,
            "game_id": game_id,
            "team_name": team_name,
            "minutes": minutes,
            "shots": shots,
            "goals": goals,
            "key_passes": key_passes,
            "assists": assists,
            "xG": xG,
            "xA": xA
        }, ignore_index=True)
        player_game_id += 1
    return player_game_df, player_game_id

def get_value_from_txt(value):
    with open(indexes_path, "r") as file:
        lines = file.readlines()

        index = 5
        if value == "start_game":
            index = 0
        elif value == "last_game":
            index = 1
        elif value == "game_id":
            index = 2
        elif value == "player_game_id":
            index = 3
        
        return int(lines[index].split("=")[1])

def update_value_in_txt(value, new_value):
    with open(indexes_path, "r") as file:
        lines = file.readlines()

    index = 5
    if value == "start_game":
        index = 0
    elif value == "last_game":
        index = 1
    elif value == "game_id":
        index = 2
    elif value == "player_game_id":
        index = 3

    lines[index] = f"{value}={new_value}\n"

    with open(indexes_path, "w") as file:
        file.writelines(lines)

def convert_string_to_date(string):
    try:
        datetime_date = datetime.datetime.strptime(string, "%b %d %Y").date()
        date_iso = datetime_date.isoformat()
        return date_iso
    except ValueError:
        raise ValueError("Invalid date format. Please use 'Aug 17 2024' format.")

def run(playwright: Playwright) -> None:

    start_game = get_value_from_txt("start_game")
    last_game = get_value_from_txt("last_game")
    game_id = get_value_from_txt("game_id")
    player_game_id = get_value_from_txt("player_game_id")

    player_game_df = pd.DataFrame(columns=["id", "player_name", "game_id", "team_name", "minutes", "shots", "goals", "key_passes", "assists", "xG", "xA"])
    games_df = pd.DataFrame(columns=["id", "understat_id", "date", "home", "away"])

    browser = playwright.chromium.launch(headless=True)

    context = browser.new_context()
    cookies = context.cookies()

    page = context.new_page()

    game_number = start_game
    while game_number <= last_game:
        page.goto(base_url + str(game_number))
        error_404_is_visible = page.get_by_text("404 The page you requested").is_visible()
        if not error_404_is_visible:
            league = page.locator("xpath=//html/body/div[1]/div[3]/ul/li[2]/a").inner_text()
            date_string = page.locator("xpath=//html/body/div[1]/div[3]/ul/li[3]").inner_text()

            home = page.locator("xpath=//html/body/div[1]/div[3]/div[2]/div[2]/h3/a").inner_text()
            away = page.locator("xpath=//html/body/div[1]/div[3]/div[2]/div[3]/h3/a").inner_text()

            date = convert_string_to_date(date_string)

            if league and league == "EPL":
                table = page.locator("xpath=//html/body/div[1]/div[3]/div[4]/div/div[2]/table/tbody[1]")
                rows = table.locator("tr")
                
                for i in range(1,3):
                    team_element = page.locator(f"xpath=//html/body/div[1]/div[3]/div[4]/div/div[1]/div/label[{i}]")
                    team_element.click()

                    team = team_element.inner_text()

                    if i == 1:
                        team = home
                    else:
                        team = away
                    player_game_df, player_game_id = get_data_from_players(table, rows, player_game_df, player_game_id, game_id, team)

                games_df = games_df._append({
                    "id": game_id,
                    "understat_id": game_number,
                    "date": date,
                    "home": home,
                    "away": away
                }, ignore_index=True)

                game_id += 1

            if (game_number - start_game + 1) % 10 == 0:
                if not player_game_df.empty and not games_df.empty:
                    player_game_df.to_csv(player_game_df_path, index=False)
                    games_df.to_csv(games_df_path, index=False)
                update_value_in_txt("start_game", game_number)
                update_value_in_txt("game_id", game_id)
                update_value_in_txt("player_game_id", player_game_id)
        game_number += 1
    if not player_game_df.empty and not games_df.empty:
        player_game_df.to_csv(player_game_df_path, index=False)
        games_df.to_csv(games_df_path, index=False)
    update_value_in_txt("start_game", game_number)
    update_value_in_txt("game_id", game_id)
    update_value_in_txt("player_game_id", player_game_id)

    context.close()
    browser.close()

def scrape_understat_data():
    with sync_playwright() as playwright:
        run(playwright)