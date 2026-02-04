import nfl_data_py as nfl
import pandas as pd


pd.set_option('display.max_rows',None)
data = nfl.import_seasonal_data([2024])
print(list(data.columns))

seasonal_data = nfl.import_seasonal_data([2024])

weekly = nfl.import_weekly_data([2024], columns = ["player_id","player_name"])

player_names = weekly.drop_duplicates(subset = "player_id")

seasonal_with_names = seasonal_data.merge(
    player_names,
    on = "player_id",
    how = "left"
)

passing_yards = seasonal_with_names[seasonal_with_names["passing_yards"]>0]

print(passing_yards[["player_name", "passing_yards"]].sort_values("passing_yards"))