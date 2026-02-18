import nfl_data_py as nfl
import pandas as pd

def sacks_qb_weekly(year, week):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    sacks = nfl.import_weekly_data([year])
    sacks = sacks[["week", "player_id", "player_name", "recent_team", "position", "sacks", "sack_yards", "sack_fumbles"]]

    sacks = sacks[sacks["sacks"] > 0]
    sacks = sacks[sacks["week"] == week]
    return sacks.sort_values(["recent_team", "position", "player_name"]).to_string(index=False)

if __name__ == "__main__":
    print(sacks_qb_weekly(2024, 1))
