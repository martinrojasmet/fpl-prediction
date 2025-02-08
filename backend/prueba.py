import pandas as pd

# Cargar los datos
final_understat_game_df = pd.read_csv("./data/final/understat_games.csv")
players_2425_df = pd.read_csv("./data/final/2425_players_data.csv")

# Filtrar la temporada 2019-20
players_19_20 = players_2425_df[players_2425_df["season"] == "2019-20"].copy()

# Iterar y corregir valores NaN
for index, row in players_19_20.iterrows():
    if pd.notna(row["local_understat_id"]):
        gw_value = final_understat_game_df.loc[final_understat_game_df["id"] == row["local_understat_fixture"], "gw"].values
        
        if len(gw_value) > 0:  # Verificar que haya un valor antes de asignarlo
            players_19_20.at[index, "gw"] = gw_value[0]

# Reemplazar los datos originales
players_2425_df.loc[players_2425_df["season"] == "2019-20", "gw"] = players_19_20["gw"]

# Guardar el archivo corregido
players_2425_df.to_csv("./data/final/2425_players_data.csv", index=False)

# Comprobar si los valores de 'gw' fueron actualizados correctamente
print("Valores únicos de 'gw' después de la actualización:", players_2425_df["gw"].unique())
