import nfl_data_py as nfl
import pandas as pd

def passing_yards_in_season(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id","player_name", "recent_team", "position"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    passing_yards = seasonal_with_names[seasonal_with_names["passing_yards"] > 0]
    return passing_yards[["player_name","recent_team","position", "passing_yards"]].sort_values("recent_team")

def rushing_stats(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team", "position"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    rushing_yards = seasonal_with_names[seasonal_with_names["rushing_yards"] > 0]
    rushing_yards = rushing_yards[["player_name", "recent_team", "position", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles","rushing_fumbles_lost"]]
    return rushing_yards.to_string(index=False)

def attempts_completions(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([2024])
    weekly = nfl.import_weekly_data([2024], columns=["player_id", "player_name"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    percentage = seasonal_with_names[seasonal_with_names["attempts"] > 0]
    percentage = percentage[["player_name", "completions", "attempts"]]
    percentage["completion_pct"] = (percentage["completions"] / percentage["attempts"] * 100).round(2)
    percentage = percentage.sort_values("attempts")
    return percentage

def TD_INT_ratio(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    TDI = seasonal_with_names[seasonal_with_names["passing_tds"] > 0]
    TDI = TDI[["player_name", "passing_tds", "interceptions"]]

    TDI["ratio"] = (TDI["passing_tds"] / TDI["interceptions"]).round(2)
    TDI.loc[TDI["interceptions"] == 0, "ratio"] = "NO INT"
    TDI = TDI.sort_values("passing_tds")
    return TDI

def receiving_stats(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    seasonal_data = nfl.import_seasonal_data([2024])
    weekly = nfl.import_weekly_data([2024], columns=["player_id", "player_name"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    YAC = seasonal_with_names[seasonal_with_names["targets"] > 0]
    YAC = YAC[
        ["player_name", "receptions", "targets", "receiving_yards", "receiving_yards_after_catch", "receiving_tds"]]

    YAC["rec_to_tar"] = (YAC["receptions"] / YAC["targets"]).round(2)
    YAC["rec_to_yards"] = (YAC["receptions"] / YAC["receiving_yards"]).round(2)
    YAC = YAC.sort_values("targets")
    return YAC.to_string(index = False)

def special_teams_tds(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([2024])
    weekly = nfl.import_weekly_data([2024], columns=["player_id", "player_name", "recent_team"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    total = seasonal_with_names[seasonal_with_names["special_teams_tds"] > 0]
    total = total[["player_id", "player_name", "recent_team", "special_teams_tds"]].sort_values("recent_team")
    return total

def sacks_by_qb(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    seasonal_data = nfl.import_seasonal_data([2024])
    weekly = nfl.import_weekly_data([2024], columns=["player_id", "player_name", "recent_team"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    sacks = seasonal_with_names[seasonal_with_names["sacks"] > 0]
    sacks = sacks[["player_id", "player_name", "recent_team", "sacks", "sack_yards", "sack_fumbles", "sack_fumbles_lost"]].sort_values(
        "sacks")
    return sacks.to_string(index = False)