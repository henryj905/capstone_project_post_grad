import nfl_data_py as nfl
import pandas as pd


def passing_yards_in_season(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team", "position"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    passing_yards = seasonal_with_names[seasonal_with_names["passing_yards"] > 0]
    return passing_yards[["player_name", "recent_team", "position", "passing_yards"]].sort_values("recent_team")


def rushing_stats(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team", "position"])
    weekly = weekly.drop_duplicates(subset="player_id")
    efficiency = nfl.import_ngs_data("rushing", [2024])
    efficiency = efficiency[["player_gsis_id", "efficiency"]]
    efficiency_avg = efficiency.groupby(["player_gsis_id"], as_index=False)["efficiency"].mean()
    efficiency_sorted = efficiency_avg.sort_values("player_gsis_id")
    efficiency_sorted = efficiency_sorted.rename(columns={"player_gsis_id": "player_id"})

    seasonal_data = seasonal_data.merge(
        weekly, 
        on="player_id", 
        how="left"
    )
    seasonal_data = seasonal_data.merge(
        efficiency_sorted,
        on="player_id",
        how="left"
    )
    seasonal_data = seasonal_data.dropna(subset=["efficiency"])
    rushing_yards = seasonal_data[seasonal_data["rushing_yards"] > 0]
    rushing_yards["YPC"] = (rushing_yards["rushing_yards"] / rushing_yards["carries"]).round(2)
    rushing_yards = rushing_yards[["player_name", "recent_team", "position", "carries", "rushing_yards", "YPC",
                                   "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", "efficiency"]]
    return rushing_yards.to_string(index=False, col_space=12)


def attempts_completions(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name"])
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


def td_int_ratio(year):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    tdi = seasonal_with_names[seasonal_with_names["passing_tds"] > 0]
    tdi = tdi[["player_name", "passing_tds", "interceptions"]]

    tdi["ratio"] = (tdi["passing_tds"] / tdi["interceptions"]).round(2)
    tdi.loc[tdi["interceptions"] == 0, "ratio"] = "NO INT"
    tdi = tdi.sort_values("passing_tds")
    return tdi


def receiving_stats(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    yac = seasonal_with_names[seasonal_with_names["targets"] > 0]
    yac = yac[
        ["player_name", "receptions", "targets", "receiving_yards", "receiving_yards_after_catch", "receiving_tds"]]

    yac["rec_to_tar"] = (yac["receptions"] / yac["targets"]).round(2)
    yac["rec_to_yards"] = (yac["receptions"] / yac["receiving_yards"]).round(2)
    yac = yac.sort_values("targets")
    yac = yac.to_strinf(index=False)
    return yac


def sacks_by_qb(year):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team"])
    player_names = weekly.drop_duplicates(subset="player_id")
    seasonal_with_names = seasonal_data.merge(
        player_names,
        on="player_id",
        how="left"
    )
    sacks = seasonal_with_names[seasonal_with_names["sacks"] > 0]
    sacks = sacks[["player_id", "player_name", "recent_team", "sacks", "sack_yards", "sack_fumbles",
                   "sack_fumbles_lost"]].sort_values("sacks")
    sacks = sacks.to_string(index=False)
    return sacks
