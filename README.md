# Fpl Prediction

This is a fun project I’ve wanted to tackle for a while: a Fantasy Premier League (FPL) prediction system. My goal was to build as much of an end-to-end solution as I could, but I don’t think I am capable of tracking and calculating the stats from the actual match videos yet; hopefully pretty soon I'll be able to. I started with the data provided by [vaastav][vaastav] in his [repository][repo_url] as a foundation, since I wasn’t sure where else to access the historic official FPL game data. To address gaps in expected goals (xG) and expected assists (xA) data for seasons prior to 2022-23, I complemented the dataset by scraping [understat.com][understat].

After cleaning and merging the official FPL data with Understat’s metrics, I developed a model to predict players’ points for the upcoming gameweek. The predictions factor in the player’s historical performance and their track record against specific opponents. I used XGBoost and Linear Regression algorithms to generate these forecasts.

On the other hand, I developed a game winner prediction model for the upcoming gameweek based on team statistics. The model utilizes an XGBoost Classifier and rolling averages to generate predictions.

The points's results are displayed on a simple webpage featuring an interactive graph of the player’s performance history and predicted points, as well as the basic details like the player name and opponent. Additionally, the winner predictions are presented in a straightforward format, with the winner highlighted in green and a tie in gray.

I hope the data I gathered and merged can be useful to you, in any projects you may undertake. As I gain more experience and time, I plan to refine the model’s accuracy, add new features, and experiment with different methods to improve its performance.

![FPL Point Prediction Example from 2025-02-09](https://github.com/martinrojasmet/fpl-prediction/raw/main/fpl-prediction-points.gif "FPL Point Prediction Example from 2025-02-09")

![FPL Game Prediction Example from 2025-02-09](https://github.com/martinrojasmet/fpl-prediction/raw/main/fpl-prediction-games.png "FPL Game Prediction Example from 2025-02-09")


[repo_url]: https://github.com/vaastav/Fantasy-Premier-League
[vaastav]: https://github.com/vaastav
[understat]: https://understat.com/