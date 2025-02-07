import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

# PREDICTION

data = pd.read_csv('games_data_GA_rolling.csv')

xgb = XGBClassifier(n_estimators=50, random_state=10)

amount_training = .92
train = data[:int(len(data)*amount_training)]
test = data[int(len(data)*amount_training):]

normal_predictors = ['home_team_code', 'away_team_code']

predictors = ['home_xG', 'away_xG', 'home_xA', 'away_xA', 'home_Goals', 'away_Goals', 'home_Assists', 'away_Assists']
rolling_predictors = ['rolling_home_xG', 'rolling_away_xG', 'rolling_home_xA', 'rolling_away_xA', 'rolling_home_Goals', 'rolling_away_Goals', 'rolling_home_Assists', 'rolling_away_Assists']
train_predictors = normal_predictors + predictors
test_predictors = normal_predictors + predictors

xgb.fit(train[train_predictors], train['result'])
test.drop(columns=predictors, inplace=True)

for word in rolling_predictors:
    test.rename(columns={word: word[8:]}, inplace=True)

preds = xgb.predict(test[test_predictors])

combined = pd.DataFrame(dict(actual=test['result'], predicted=preds))

precision = precision_score(test['result'], preds, average='macro')

print(precision)
combined = pd.DataFrame(dict(actual=test['result'], predicted=preds))
print(pd.crosstab(combined['actual'], combined['predicted']))


# # acc = accuracy_score(test['result'], preds)

# # print(acc)

# # combined = pd.DataFrame(dict(actual=test['result'], predicted=preds))

# # print(pd.crosstab(combined['actual'], combined['predicted']))

# # prec = precision_score(test['result'], preds, average='macro')

# # print(prec)

# # unique_teams = pd.concat([data['home_team_code'], data['away_team_code']]).unique()

# for team in unique_teams:
#     grouped_matches = data[(data['home_team_code'] == team) | (data['away_team_code'] == team)]

# print(grouped_matches)
# Create rolling averages for each team
# rolling_window = 5

# data_copy = data.copy()

# for team in unique_teams:
#     print('equipo ', team)
#     team_data = data[(data['home_team_code'] == team)].copy().reset_index(drop=True)
#     team_data.drop(columns=['away_team_code', 'away_xA', 'away_Assists', 'away_Goals', 'away_xG','understat_id','date','home','away'], inplace=True)
#     team_data.rename(columns={'home_team_code': 'team_code', 'home_xA': 'team_xA', 'home_Assists': 'team_Assists', 'home_Goals': 'team_Goals', 'home_xG':'team_xG'}, inplace=True)
#     # print(team_data)

#     team_data_away = data[(data['away_team_code'] == team)].copy().reset_index(drop=True)
#     team_data_away.drop(columns=['home_team_code', 'home_xA', 'home_Assists', 'home_Goals', 'home_xG','understat_id','date','home','away'], inplace=True)
#     team_data_away.rename(columns={'away_team_code': 'team_code', 'away_xA': 'team_xA', 'away_Assists': 'team_Assists', 'away_Goals': 'team_Goals', 'away_xG':'team_xG'}, inplace=True)
#     # print(team_data_away)

#     team_data = pd.concat([team_data, team_data_away]).reset_index(drop=True)

#     team_data = team_data.sort_values(by='id')

#     team_data['team_xG'] = team_data['team_xG'].rolling(window=rolling_window).mean()
#     team_data['team_xA'] = team_data['team_xA'].rolling(window=rolling_window).mean()
#     team_data['team_Goals'] = team_data['team_Goals'].rolling(window=rolling_window).mean()
#     team_data['team_Assists'] = team_data['team_Assists'].rolling(window=rolling_window).mean()

#     print(team_data)

#     for i in range(0, len(team_data)):
#         data_index = data[data['id'] == team_data.at[i, 'id']].index[0]
#         # print(data_index)
#         if data.at[data_index, 'home_team_code'] == team_data.at[i, 'team_code']:
#             data_copy.at[data_index, 'rolling_home_xG'] = team_data.at[i, 'team_xG']
#             data_copy.at[data_index, 'rolling_home_xA'] = team_data.at[i, 'team_xA']
#             data_copy.at[data_index, 'rolling_home_Goals'] = team_data.at[i, 'team_Goals']
#             data_copy.at[data_index, 'rolling_home_Assists'] = team_data.at[i, 'team_Assists']
#         else:
#             data_copy.at[data_index, 'rolling_away_xG'] = team_data.at[i, 'team_xG']
#             data_copy.at[data_index, 'rolling_away_xA'] = team_data.at[i, 'team_xA']
#             data_copy.at[data_index, 'rolling_away_Goals'] = team_data.at[i, 'team_Goals']
#             data_copy.at[data_index, 'rolling_away_Assists'] = team_data.at[i, 'team_Assists']

# data_copy.to_csv('games_data_GA_rolling.csv', index=False)