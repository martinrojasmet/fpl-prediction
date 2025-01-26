import pandas as pd
import requests
import os

fpl_data_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
fpl_image_url = 'https://resources.premierleague.com/premierleague/photos/players/110x140/p'

player_data = pd.read_csv('./data/pivot/players.csv')

def get_opta_ids():
    fpl_json = requests.get(fpl_data_url).json()
    player_json = fpl_json['elements']

    for player in player_json:
        player_id = player['id']
        opta_id = player['photo'][:-4]
        player_data.loc[player_data['fpl_2024-25'] == player_id, 'opta_id'] = opta_id

    player_data.to_csv('./data/pivot/players.csv', index=False)

def get_images():
    unique_opta_ids = player_data['opta_id'].unique()

    for opta_id in unique_opta_ids:
        image_path = './assets/player_images/' + str(opta_id) + '.png'
        if not os.path.exists(image_path):
            image_url = fpl_image_url + str(opta_id) + '.png'
            image = requests.get(image_url)
            if image.headers['Content-Type'] == 'image/png':
                with open(image_path, 'wb') as f:
                    f.write(image.content)

# tmp
def delete_not_images():
    for filename in os.listdir('./assets/player_images/'):
        if filename.endswith('.png'):
            try:
                with open('./assets/player_images/' + filename, 'rb') as f:
                    content = f.read()
                    if b'Access Denied' in content:
                        os.remove('./assets/player_images/' + filename)
            except:
                continue
        else:
            os.remove('./assets/player_images/' + filename)

def update_images_locally():
    get_opta_ids()
    get_images()