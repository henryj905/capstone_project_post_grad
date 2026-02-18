import nfl_data_py as nfl
import pandas as pd

def passing_weekly(year, week):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    weekly = nfl.import_weekly_data([year])
    weekly = weekly[["week", "player_id", "player_name", "recent_team", "position", "completions", "attempts", "passing_yards",
                     "passing_tds", "interceptions"]]
    efficiency = nfl.import_ngs_data("passing", [year])
    efficiency = efficiency[["player_gsis_id", "completion_percentage", "passer_rating", "week"]]
    efficiency = efficiency.rename(columns={"player_gsis_id": "player_id"})
    efficiency = efficiency.drop_duplicates()
    weekly = weekly.merge(
        efficiency,
        on=["player_id", "week"],
        how="left"
    )

    weekly = weekly[weekly["attempts"] > 0]
    weekly = weekly[weekly["week"] == week]

    return weekly.sort_values(["recent_team", "position", "player_name"]).to_string(index=False)

def rushing_weekly(year, week):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    weekly = nfl.import_weekly_data([year])
    weekly = weekly[["week", "player_id", "player_name", "recent_team", "position", 'carries', 'rushing_yards', 'rushing_tds', 'rushing_fumbles']]
    efficiency = nfl.import_ngs_data("rushing", [year])
    efficiency = efficiency[["player_gsis_id", "efficiency", "week"]]
    efficiency = efficiency.rename(columns={"player_gsis_id": "player_id"})
    efficiency = efficiency.drop_duplicates()
    weekly = weekly.merge(
        efficiency,
        on=["player_id", "week"],
        how="left"
    )

    weekly = weekly[weekly["carries"] > 0]
    weekly = weekly[weekly["week"] == week]

    return weekly.sort_values(["recent_team", "position", "player_name"]).to_string(index=False)


def receiving_weekly(year, week):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    weekly = nfl.import_weekly_data([year])
    weekly = weekly[
        ["week", "player_id", "player_name", "recent_team", "position", 'targets', 'receptions', 'receiving_yards',
         'receiving_tds']]

    weekly = weekly[weekly["targets"] > 0]
    weekly = weekly[weekly["week"] == week]

    return weekly.sort_values(["recent_team", "position", "player_name"]).to_string(index=False)

def sacks_qb_weekly(year, week):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    sacks = nfl.import_weekly_data([year])
    sacks = sacks[["week", "player_id", "player_name", "recent_team", "position", "sacks", "sack_yards", "sack_fumbles"]]

    sacks = sacks[sacks["sacks"] > 0]
    sacks = sacks[sacks["week"] == week]
    return sacks.sort_values(["recent_team", "position", "player_name"]).to_string(index=False)
