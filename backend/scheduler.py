import requests
from datetime import datetime, timedelta
import json
import os
import logging

utils_path = "./utils/"
run_dates = utils_path + "run_dates.json"

folder_path = "/home/martin/Documents/GitHub/fpl4/"
sh_file_path = folder_path + "run_print_gw.sh"

def get_latest_dates():
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)
    fixtures = response.json()

    latest_dates = {}
    for fixture in fixtures:
        gw = fixture['event']
        kickoff_time = datetime.strptime(fixture['kickoff_time'], "%Y-%m-%dT%H:%M:%SZ")
        kickoff_time = kickoff_time - timedelta(hours=4) # Convert to Caracas time
        kickoff_time = kickoff_time - timedelta(hours=4) # After the game
        kickoff_time = kickoff_time + timedelta(hours=12) # Add half a day to run the code
        if gw not in latest_dates or kickoff_time > latest_dates[gw]:
            latest_dates[gw] = kickoff_time

    with open(run_dates, 'w') as f:
        json.dump(latest_dates, f, indent=4, default=str)

def schedule_one_time_job():
    with open(run_dates, 'r') as f:
        dates = json.load(f)

    # Delete all previous cron jobs
    os.system('atrm $(atq | cut -f1)')
    
    for gw, date_str in dates.items():
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        at_time = date.strftime('%H:%M %d.%m.%Y')
        command = f'echo "python {folder_path}pipeline.py" | at {at_time}'
        try:
            result = os.system(command)
        except Exception as e:
            logging.error(f'Failed to schedule job for GW {gw}: {e}')
            print(f'Failed to schedule job for GW {gw}: {e}')

def schedule_scripts():
    get_latest_dates()
    schedule_one_time_job()