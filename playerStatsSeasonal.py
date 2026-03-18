import nfl_data_py as nfl
import pandas as pd


def passing_stats_season(year, player):
    pd.set_option('display.max_rows', None)
    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team",
                                                     "position"]).drop_duplicates(subset="player_id")

    data = seasonal_data.merge(
        weekly,
        on="player_id",
        how="left"
    )

    data = data[data["attempts"] > 0]

    data["completion_pct"] = (
        data["completions"] / data["attempts"] * 100
    ).round(2)

    efficiency = nfl.import_ngs_data("passing", [2024])
    efficiency = efficiency[["player_gsis_id", "passer_rating"]]
    efficiency_avg = efficiency.groupby(["player_gsis_id"], as_index=False)["passer_rating"].mean()
    efficiency_avg = efficiency_avg.rename(columns={"player_gsis_id": "player_id"})

    data = data.merge(
        efficiency_avg,
        on="player_id",
        how="left"
    )
    data = data[data["player_name"] == player]
    print(data[['player_name']])

    return data[["player_name", "recent_team", "position", "passing_yards", "completions", "attempts", "completion_pct",
                 "passing_tds", "interceptions", "passer_rating"]].sort_values("recent_team")

def rushing_stats_season(year, team):
    team = team.upper()
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

    rushing_yards = rushing_yards[rushing_yards["recent_team"] == team]

    return rushing_yards.sort_values("recent_team")


def receiving_stats_season(year, team):
    team = team.upper()

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
    yac = seasonal_with_names[seasonal_with_names["targets"] > 0]
    yac = yac[
        ["player_id", "player_name", "recent_team", "receptions", "targets", "receiving_yards", "receiving_yards_after_catch", "receiving_tds"]]

    yac["avg_completion_pct"] = (yac["receptions"] / yac["targets"]).round(2)
    yac["avg_yards_per_rec"] = (yac["receiving_yards"] / yac["receptions"]).round(2)

    data = nfl.import_ngs_data("receiving", [2024])

    separation = data[["player_gsis_id", "avg_separation"]]
    separation_avg = separation.groupby(["player_gsis_id"], as_index=False)["avg_separation"].mean()
    separation_avg = separation_avg.rename(columns={"player_gsis_id": "player_id"})

    yac = yac.merge(
        separation_avg,
        on="player_id",
        how="left"
    )

    yac = yac.sort_values("targets")
    yac = yac
    yac = yac[yac["recent_team"] == team]

    return yac.sort_values("recent_team")


def sacks_by_qb_season(year, team):
    team = team.upper()

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
    sacks = sacks[sacks["recent_team"] == team]

    sacks = sacks[["player_id", "player_name", "recent_team", "sacks", "sack_yards", "sack_fumbles",
                   "sack_fumbles_lost"]].sort_values("recent_team")
    return sacks


def special_teams_tds_season(year, team):
    team = team.upper()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    seasonal_data = nfl.import_seasonal_data([year])
    weekly = nfl.import_weekly_data([year], columns=["player_id", "player_name", "recent_team"]).drop_duplicates()

    seasonal_data = seasonal_data.merge(
        weekly,
        on="player_id",
        how="left"
    )
    seasonal_data = seasonal_data[["player_id", "player_name", "recent_team", "special_teams_tds"]].sort_values("recent_team")
    seasonal_data = seasonal_data[seasonal_data["recent_team"] == team]

    seasonal_data = seasonal_data[seasonal_data["special_teams_tds"] > 0]

    return seasonal_data
